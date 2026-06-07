from flask import Blueprint, request, render_template, redirect
from models import db, Post

posts = Blueprint('posts', __name__)

# CREATE POST
@posts.route('/create', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content']
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/')

    return render_template('create_post.html')


# DELETE POST
@posts.route('/delete/<int:id>')
def delete_post(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')