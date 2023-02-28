from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.user import User
from flask_app.models.route import Route
from flask_app.models.comment import Comment
from flask_bcrypt import Bcrypt

import os
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session:
        flash('Please log in first!', 'login')
        return redirect('/')
    data = {'id':session['user_id']}
    return render_template('dashboard.html', user=User.get_user(data), all_routes=Route.get_with_creator())

@app.route('/register', methods=['post'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['regpassword'])
    print(pw_hash)
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
    }
    if not User.validate_registration(request.form):
        return redirect('/')
    user_id = User.add_user(data)
    session['user_id'] = user_id
    session['first_name'] = data['first_name']
    session['last_name'] = data['last_name']
    return redirect('/dashboard')

@app.route('/login', methods=['post'])
def login():
    data = {'email':request.form['email']}
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash('Email does not have an associated account.', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash('Invalid email/password combination.', 'login')
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    session['last_name'] = user_in_db.last_name
    return redirect('/dashboard')

@app.route('/logout', methods=['get', 'post'])
def logout():
    session.clear()
    return redirect('/')

@app.route('/create')
def create_page():
    if not session:
        flash('Please log in first!', 'login')
        return redirect('/')
    data = {'id': session['user_id']}
    return render_template('create.html', user=User.get_user(data))

@app.route('/create/submit', methods=['post'])
def create():
    data = {
            'name': request.form['name'],
            'type': request.form['type'],
            'date_completed': request.form['date_completed'],
            'difficulty': request.form['difficulty'],
            'crag': request.form['crag'],
            'danger': request.form['danger'],
            'rating': request.form['rating'],
            'mountain_project': request.form['mountain_project'],
            'comment': request.form['comment'],
            'user_id': session['user_id']
    }
    if not Route.validate_route(data):
        return redirect('/create')
    Route.add_route(data)
    return redirect('/dashboard')

@app.route('/viewroute/<int:route_id>', methods=['get'])
def view_sighting(route_id):
    data = {
        'id' : route_id
    }
    return render_template('oneroute.html', route = Route.get_one_route(data), all_comments = Comment.get_comments(data))

@app.route('/update/<int:route_id>', methods=['get'])
def edit_page(route_id):
    data= {'id':route_id}
    return render_template('update.html', route=Route.get_one_route(data))

@app.route('/update/<int:route_id>', methods=['post'])
def edit_route(route_id):
    print(request.form)
    data={
        'id': route_id,
        'name': request.form['name'],
        'type': request.form['type'],
        'date_completed': request.form['date_completed'],
        'difficulty': request.form['difficulty'],
        'crag': request.form['crag'],
        'danger': request.form['danger'],
        'rating': request.form['rating'],
        'mountain_project': request.form['mountain_project'],
        'comment': request.form['comment'],
    }
    if not Route.validate_route(data):
        return redirect(request.referrer)
    Route.update_route(data)
    flash('Route has been successfully updated', 'route')
    return redirect('/dashboard')

@app.route('/delete/<int:route_id>', methods=['get'])
def delete_route(route_id):
    data = {
        'id': route_id
    }
    Route.delete_route(data)
    flash('Route has been successfully deleted', 'route')
    return redirect('/dashboard')

@app.route('/viewroute/<int:route_id>/comment', methods=['GET','POST'])
def add_guest_comment(route_id):
    data = {
        'guest_comment' : request.form['guest_comment'],
        'route_id' : route_id,
        'user_id' : session['user_id']
    }
    Comment.add_comment(data)
    return redirect(request.referrer)

