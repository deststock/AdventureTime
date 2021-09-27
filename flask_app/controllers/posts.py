from flask_app.models.post import Post
from flask_app import app 
from flask import render_template, redirect, request, session, flash, jsonify
from flask_app.models.user import User 

@app.route('/posted', methods =['POST'])
def post(): 
    data = {
        "location": request.form['location'],
        "content": request.form.get('editordata'),
        "user_id": session['user_id']
    }
    Post.save(data)
    return redirect('/dashboard')

@app.route('/<int:id>/comment', methods =['POST'])
def add_comment(id): 
    data = {
        "post_id": id,
        "content": request.form.get('editordata'),
        "user_id": session['user_id']
    }
    Post.add_comment(data)
    return redirect(f"/{id}/view")

@app.route ('/post')
def new_post():
    return render_template('new_post.html')

@app.route('/dashboard/<int:id>/delete')
def delte_post(id):
    data = {
        "id": id
    }
    Post.delete_post(data)
    return redirect('/dashboard')

@app.route('/profile/<int:id>/delete')
def delete_post_profile(id):
    data = {
        "id": id
    }
    Post.delete_post(data)
    return redirect(f"/{session['user_id']}/profile")

@app.route('/api/<int:id>/like')
def like_post(id):
    data = {
        "post_id": id,
        "user_id": session['user_id']
    }
    Post.like_post(data)    
    return redirect('/dashboard')

@app.route('/api/profile/<int:id>/like')
def like_post_profile(id):
    data = {
        "post_id": id,
        "user_id": session['user_id']
    }
    Post.like_post(data)    
    return redirect(f"/{session['user_id']}/profile")

@app.route('/<int:id>/view')
def view_post(id):
    data = {
        "id": id
    }
    return render_template('view_post.html', posts = Post.get_post(data), user = User.get_by_id(data), comments = Post.get_comments(data))

