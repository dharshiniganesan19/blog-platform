from flask import Blueprint, request, render_template
from models import db, Comment, Post

comments = Blueprint('comments', __name__)

# VIEW + ADD COMMENTS
@comments.route('/post/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        comment = Comment(
            text=request.form['text'],
            post_id=id
        )
        db.session.add(comment)
        db.session.commit()

    all_comments = Comment.query.filter_by(post_id=id).all()

    return render_template(
        'post_detail.html',
        post=post,
        comments=all_comments
    )