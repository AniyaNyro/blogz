from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:giraFFe17@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'giraFFE17'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    pw_hash = db.Column(db.String(120))
    blog_posts = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_text  = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text):
        self.blog_title = title
        self.blog_text = text

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['email'] = email
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route('/add-post', methods=['POST', 'GET'])
def add_post():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        post = Blog(title, text)
        db.session.add(post)
        db.session.commit()
        flash("New Blog Entry")
        return redirect('/')
    else:
        return render_template('add-post.html')

@app.route('/', methods=['POST', 'GET'])
def display_post():

    if request.method == 'POST':
        blog_title = request.form['title'] 
        blog_text = request.form['text']
        
    else:
        if request.args.get('id'):
            dog = request.args.get('id')
            post = Blog.query.get(dog)
            return render_template('post.html', post=post)
            
        blog_enteries = Blog.query.all()
        return render_template('todos.html', blog_enteries=blog_enteries)


if __name__ == '__main__':
    app.run()