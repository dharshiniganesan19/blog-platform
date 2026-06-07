from flask import Flask, render_template, request, redirect
from models import db, User, Post, Comment

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# ---------------- HOME ----------------
@app.route('/')
def home():
    posts = Post.query.all()
    return render_template('index.html', posts=posts)

# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        user = User(
            username=request.form['username'],
            password=request.form['password']
        )
        db.session.add(user)
        db.session.commit()
        return redirect('/login')

    return render_template('register.html')

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            return redirect('/')
    return render_template('login.html')

# ---------------- CREATE POST ----------------
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        post = Post(
            title=request.form['title'],
            content=request.form['content']
        )
        db.session.add(post)
        db.session.commit()
        return redirect('/')

    return render_template('create_post.html')

# ---------------- POST DETAIL ----------------
@app.route('/post/<int:id>', methods=['GET', 'POST'])
def post_detail(id):
    post = Post.query.get(id)

    if request.method == 'POST':
        comment = Comment(
            text=request.form['text'],
            post_id=id
        )
        db.session.add(comment)
        db.session.commit()

    comments = Comment.query.filter_by(post_id=id).all()
    return render_template('post_detail.html', post=post, comments=comments)

# ---------------- DELETE POST ----------------
@app.route('/delete/<int:id>')
def delete(id):
    post = Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/')

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)