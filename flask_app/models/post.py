import flask
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
from flask_app import app

class Post: 
    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.location = data['location']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def all_posts(cls):
        query = "SELECT posts.id, posts.content, posts.location, posts.user_id, users.first_name, users.last_name, users.username, users.id, count(likes.post_id) AS num_likes from posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id GROUP BY posts.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL("adventure_schema").query_db(query)
        post_info = []
        for row in results: 
            data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username": row['username'],
                "content": row['content'],
                "location": row['location'],
                "user_id": row['user_id'],
                "id": row['id'],
                "num_likes": row['num_likes']
            }
            post_info.append(data)
        return post_info

    @classmethod
    def save(cls,data): 
        query = "INSERT INTO posts (content,location, user_id) VALUES (%(content)s, %(location)s, %(user_id)s); "
        return connectToMySQL('adventure_schema').query_db(query,data)

    @classmethod 
    def get_likes(cls,data):
        query = "SELECT * FROM likes LEFT JOIN users ON user_id = users.id LEFT JOIN posts ON post_id = posts.id where post_id=%(id)s;"
        return connectToMySQL('adventure_schema').query_db(query,data)

    @classmethod
    def delete_post(cls,data):
        query = "DELETE FROM likes WHERE post_id = %(id)s;"
        connectToMySQL('adventure_schema').query_db(query,data)
        query = "DELETE FROM comments WHERE post_id = %(id)s;"
        connectToMySQL('adventure_schema').query_db(query,data)
        query = "DELETE FROM posts WHERE id = %(id)s;"
        return connectToMySQL('adventure_schema').query_db(query,data)

    @classmethod 
    def like_post(cls,data):
        query = "INSERT INTO likes (post_id, user_id) VALUES (%(post_id)s, %(user_id)s);"
        return connectToMySQL('adventure_schema').query_db(query,data)

    # @classmethod 
    # def unlike_post(cls,data):
    #     query = "DELETE FROM likes WHERE post_id = %(id)s;"
    #     return connectToMySQL('adventure_schema').query_db(query,data)

    @classmethod
    def get_post(cls,data):
        query = "SELECT posts.id, posts.content, posts.location, posts.user_id, users.first_name, users.last_name, users.username, users.id, count(likes.post_id) AS num_likes, count(comments.post_id) AS num_comments from posts LEFT JOIN users ON posts.user_id = users.id LEFT JOIN likes ON posts.id = likes.post_id LEFT JOIN comments ON posts.id = comments.post_id WHERE posts.id = %(id)s GROUP BY posts.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL('adventure_schema').query_db(query,data)
        post_info = []
        for row in results: 
            data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username": row['username'],
                "content": row['content'],
                "location": row['location'],
                "user_id": row['user_id'],
                "id": row['id'],
                "num_likes": row['num_likes'],
                "num_comments": row['num_comments']
            }
            post_info.append(data)
        return post_info

    @classmethod 
    def get_comments(cls,data):
        query= "SELECT * FROM comments LEFT JOIN users on comments.user_id = users.id WHERE post_id = %(id)s;"
        results = connectToMySQL('adventure_schema').query_db(query,data)
        print(results)
        comment_info = []
        for row in results: 
            data = {
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "username": row['username'],
                "profile_picture": row['profile_picture'],
                "content": row['content'],
                "user_id": row['user_id'],
                "id": row['id'],
            }
            comment_info.append(data)
        return comment_info

    @classmethod 
    def add_comment(cls,data):
        query = "INSERT INTO comments (content, post_id, user_id) VALUES (%(content)s, %(post_id)s, %(user_id)s);"
        return connectToMySQL('adventure_schema').query_db(query,data)