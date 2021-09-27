from flask_app.models.post import Post
from flask_app import app 
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.user import User 
import re
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/')         
def index():
    return render_template("register.html")

@app.route('/existinguser')
def newuser():
    return render_template("login.html")

@app.route('/api/user/login', methods = ['POST'])
def api_login():
    msg = {
        'status': 200
    }
    data = {
        "email": request.form['email']
    }
    user_in_db = User.get_by_email(data)
    is_valid = True
    errors = {}
    if not user_in_db:
        errors['email_error'] = "Invalid email or password."
        is_valid = False
    if len(request.form['password']) < 1: 
        errors['password_error'] = "Invalid email or password."
        is_valid = False
    if user_in_db:
        if not bcrypt.check_password_hash(user_in_db.password,request.form['password']):
            errors['password_error'] = "Invalid email or password."
            is_valid = False
    if not is_valid: 
        msg['status'] = 400
        msg['errors'] = errors
        return jsonify(msg)
    session['user_id'] = user_in_db.id
    session['user_first_name'] = user_in_db.first_name
    return jsonify(msg)


@app.route('/api/register', methods = ['POST'])
def api_register():
    msg = {
        'status': 200
    }
    is_valid = True 
    errors = {}
    if len(request.form['birthdate']) == 0: 
        errors['birthdate_error'] = "Birthdate must be entered."
        is_valid = False
    if len(request.form['location']) < 3: 
        errors['location_error'] = "Location must be at least 3 characters."
        is_valid = False
    if len(request.form['first_name']) < 3: 
        errors['first_name_error'] = "First name must be at least 3 characters."
        is_valid = False
    if len(request.form['last_name']) < 3: 
        errors['last_name_error'] = "Last name must be at least 3 characters."
        is_valid = False
    if len(request.form['username']) < 3: 
        errors['username_error'] = "Username must be at least 3 characters."
        is_valid = False
    if not EMAIL_REGEX.match(request.form['email']):
        errors['email_error'] = "Invalid email."
        is_valid = False
    if len(request.form['password']) < 8:
        errors['password_error'] = "Password must be at least 8 characters."
        is_valid = False
    if request.form['password'] != request.form['confirm_password']:
        errors['confirm_password_error'] = "Passwords do not match."
        is_valid = False
    if not is_valid:
        msg['status'] = 400
        msg['errors'] = errors
        return jsonify(msg)
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "email": request.form['email'],
        "password": pw_hash, 
        "birthdate": request.form['birthdate'],
        "location": request.form['location'],
    }
    user_id = User.save(data)
    session['user_id'] = user_id
    return jsonify(msg)

@app.route ('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_by_id(data)
    posts = Post.all_posts()
    return render_template("dashboard.html", user = user, posts = posts)

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

@app.route('/<int:id>/profile')
def myProfile(id): 
    data = {
        "id": id
    }
    return render_template('profile.html', user = User.get_by_id(data), posts = User.users_post(data))

@app.route('/<int:id>/profile/likes')
def get_likes(id):
    data = {
        "id": id
    }
    return render_template('profile_likes.html', user = User.get_by_id(data), posts = User.get_likes(data))

@app.route('/<int:id>/edit')
def edit_page(id): 
    data = {
        "id": id
    }
    return render_template('edit_profile.html', user = User.get_by_id(data))

@app.route('/<int:id>/save', methods= ['POST'])
def save_changes(id): 
    if 'user_id' not in session: 
        return redirect ('/')
    if not User.validate_edit(request.form):
        return redirect(f"/{id}/edit")
    data = { 
        "id": id,
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "username": request.form['username'],
        "birthdate": request.form['birthdate'],
        "location": request.form['location'],
        "profile_picture": request.form['profile_picture'],
        "header": request.form['header']
    }
    User.edit_user(data)
    return redirect(f"/{id}/profile")


