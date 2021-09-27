import flask
from flask_app.models import post
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.location = data['location']
        self.birthdate = data['birthdate']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']


    @staticmethod
    def validate_user(user):
        is_valid = True 
        if len(user['birthdate']) == 0: 
            flash("Birthdate must be entered.", "birthdate")
            is_valid = False
        if len(user['location']) < 3: 
            flash("Location must be at least 3 characters.", "location")
        if len(user['first_name']) < 3: 
            flash("First name must be at least 3 characters.", "first_name")
            is_valid = False
        if len(user['last_name']) < 3: 
            flash("Last name must be at least 3 characters.", "last_name")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address.", "email")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "password")
            is_valid = False
        if user['password'] != user['confirm_password']:
            flash("Passwords do not match.", "match")
            is_valid = False
        return is_valid

    @staticmethod
    def validate_edit(user):
        is_valid = True 
        if len(user['birthdate']) == 0: 
            flash("Birthdate must be entered.", "birthdate")
            is_valid = False
        if len(user['location']) < 3: 
            flash("Location must be at least 3 characters.", "location")
        if len(user['first_name']) < 3: 
            flash("First name must be at least 3 characters.", "first_name")
            is_valid = False
        if len(user['last_name']) < 3: 
            flash("Last name must be at least 3 characters.", "last_name")
            is_valid = False
        return is_valid        

    @classmethod
    def save(cls,data): 
        query = "INSERT INTO users (first_name, last_name, username, email, password, birthdate, location) VALUES (%(first_name)s, %(last_name)s,  %(username)s, %(email)s, %(password)s,  %(birthdate)s, %(location)s);"
        return connectToMySQL("adventure_schema").query_db(query,data)

    @classmethod 
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL("adventure_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod 
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL("adventure_schema").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod 
    def users_post(cls,data):
        query = "SELECT posts.id, posts.content, posts.location, posts.user_id, users.first_name, users.last_name, users.username, users.id as poster_id, count(post_id) AS num_likes from posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id WHERE posts.user_id = %(id)s GROUP BY posts.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL("adventure_schema").query_db(query,data)
        post_info = []
        for row in results: 
            data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username": row['username'],
                "content": row['content'],
                "location": row['location'],
                "post_id": row['id'],
                "user_id": row['poster_id'],
                "num_likes": row['num_likes']
            }
            post_info.append(data)
        return post_info

    @classmethod 
    def edit_user(cls, data): 
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, username = %(username)s, birthdate = %(birthdate)s, location = %(location)s, profile_picture = %(profile_picture)s, header = %(header)s WHERE id = %(id)s;"
        return connectToMySQL("adventure_schema").query_db(query,data)

    @classmethod 
    def get_likes(cls,data):
        query = "SELECT posts.id, posts.content, posts.location, posts.user_id, users.first_name, users.last_name, users.username, users.id, count(likes.post_id) AS num_likes from posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN comments ON posts.id = comments.post_id WHERE likes.user_id = %(id)s GROUP BY posts.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL('adventure_schema').query_db(query,data)
        post_info = []
        print(results)
        for row in results: 
            data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username": row['username'],
                "content": row['content'],
                "location": row['location'],
                "post_id": row['id'],
                "num_likes": row['num_likes']
            }
            post_info.append(data)
        return post_info

