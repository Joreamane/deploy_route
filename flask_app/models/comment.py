from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app.models.user import User

class Comment:
    def __init__(self,data):
        self.id = data['id']
        self.guest_comment = data['guest_comment']
        self.user_id = data['user_id']
        self.route_id = data['route_id']
        self.creator = None

    @classmethod
    def add_comment(cls,data):
        query = 'INSERT INTO comments (guest_comment, user_id, route_id, created_at, updated_at) VALUES (%(guest_comment)s, %(user_id)s, %(route_id)s, NOW(), NOW());'
        flash('Comment successfully added', 'comment')
        return connectToMySQL('route_tracker').query_db(query,data)

    @classmethod
    def get_comments(cls,data):
        query = 'SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id LEFT JOIN routes ON comments.route_id = routes.id WHERE routes.id=%(id)s;'
        results = connectToMySQL('route_tracker').query_db(query,data)
        all_comments = []
        if type(results) is not bool:
            for row in results:
                one_comment = cls(row)
                comment_creator_info = {
                    'id': row['users.id'],
                    'first_name' : row['first_name'],
                    'last_name' : row['last_name'],
                    'email' : row['email'],
                    'password' : row['password'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }
                one_comment.creator = User(comment_creator_info)
                all_comments.append(one_comment)
        return all_comments
