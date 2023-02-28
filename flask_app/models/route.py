from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User

class Route:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.crag = data['crag']
        self.type = data['type']
        self.date_completed = data['date_completed']
        self.difficulty = data['difficulty']
        self.rating = data['rating']
        self.danger = data['danger']
        self.mountain_project = data['mountain_project']
        self.comment = data['comment']
        self.user_id = session['user_id']
        self.creator = None
        self.guest_comments = []

    @classmethod
    def add_route(cls,data):
        query = 'INSERT INTO routes (name, crag, type, date_completed, difficulty, rating, danger, mountain_project, comment, user_id, created_at, updated_at) VALUES (%(name)s, %(type)s, %(crag)s, %(date_completed)s, %(difficulty)s, %(rating)s, %(danger)s, %(mountain_project)s, %(comment)s, %(user_id)s, NOW(), NOW());'
        return connectToMySQL('route_tracker').query_db(query, data)

    @classmethod
    def get_routes(cls,data):
        query = 'SELECT * FROM users LEFT JOIN routes ON routes.user_id = users.id WHERE users.id=%(id)s;'
        results = connectToMySQL('route_tracker').query_db(query, data)
        user_routes = []
        for row in results:
            route_data = {
                'id': row['routes.id'],
                'name': row['name'],
                'crag': row['crag'],
                'type': row['type'],
                'date_completed': row['date_completed'],
                'difficulty': row['difficulty'],
                'rating': row['rating'],
                'danger': row['danger'],
                'mountain_project': row['mountain_project'],
                'comment': row['comment'],
                'user_id': row['user_id'],
                'created_at': row['routes.created_at'],
                'updated_at': row['routes.updated_at'],
            }
            user_routes.append(route_data)
        return user_routes

    @classmethod
    def get_with_creator(cls):
        query = 'SELECT * FROM routes JOIN users ON routes.user_id = users.id;'
        results = connectToMySQL('route_tracker').query_db(query)
        all_routes = []
        for row in results:
            one_route = cls(row)
            one_route_creator_info = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            one_route.creator = User(one_route_creator_info)
            all_routes.append(one_route)
        return all_routes

    @classmethod
    def get_one_route(cls,data):
        query = 'SELECT * FROM routes JOIN users ON routes.user_id = users.id WHERE routes.id=%(id)s;'
        return connectToMySQL('route_tracker').query_db(query, data)

    @classmethod
    def delete_route(cls,data):
        query = 'DELETE FROM routes WHERE id=%(id)s;'
        return connectToMySQL('route_tracker').query_db(query, data)

    @classmethod
    def update_route(cls,data):
        query = 'UPDATE routes SET name=%(name)s, crag=%(crag)s, type=%(type)s, date_completed=%(date_completed)s, difficulty=%(difficulty)s, rating=%(rating)s, danger=%(danger)s, mountain_project=%(mountain_project)s, comment=%(comment)s, updated_at=NOW() WHERE id=%(id)s;'
        return connectToMySQL('route_tracker').query_db(query, data)

    @staticmethod
    def validate_route(route):
        is_valid = True
        if len(route['name']) <1:
            flash('Please enter a name for your climb', 'route_creation')
            is_valid = False
        if len(route['crag']) <1:
            flash('Please enter the location of the climb', 'route_creation')
            is_valid = False
        if len(route['type']) <1:
            flash('Please select a type for your climb', 'route_creation')
            is_valid = False
        if len(route['date_completed']) <1:
            flash('Please enter a date for your climb', 'route_creation')
            is_valid = False
        if len(route['difficulty']) <1:
            flash('Please select a difficulty for your climb', 'route_creation')
            is_valid = False
        if len(route['rating']) <1:
            flash('Please select a rating for your climb', 'route_creation')
            is_valid = False
        if len(route['danger']) <1:
            flash('Please select a danger level for your climb', 'route_creation')
            is_valid = False
        return is_valid
