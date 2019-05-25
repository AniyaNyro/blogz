from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:giraFFe17@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'giraFFE17'

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    blog_posts = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    blog_title = db.Column(db.String(120))
    blog_text  = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, text, owner):
        self.blog_title = title
        self.blog_text = text
        self.owner = owner

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['user'] = user.username
            flash("Logged in")
            return redirect('/')
        else:
            flash('User password incorrect, or user does not exist', 'error')

    return render_template('login.html')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
    ##line 55 is trouble for writing to db
        username_db_count = User.query.filter_by(username=username).count()
        if username_db_count > 0:
            flash('yikes! "' + username + '" is already taken and password reminders are not implemented')
            return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.username
        return redirect("/")
    else:
        return render_template('register.html')

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/")

@app.route('/new-post', methods=['POST', 'GET'])
def add_post():
   
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        owner = User.query.filter_by(username=session['user']).first()
        post = Blog(title, text, owner)
        db.session.add(post)
        db.session.commit()
        flash("New Blog Entry")
        return redirect('/')
    else:
        return render_template('new-post.html')

@app.route('/all-post', methods=['POST', 'GET'])
def display_posts():

    if request.method == 'POST':
        blog_title = request.form['title']
        blog_text = request.form['text']
        username = request.form['username'] 
    
    else:
        if request.args.get('id'):
            dog = request.args.get('id')
            post = Blog.query.get(dog)
            return render_template('post.html',post=post)

        if request.args.get('username'):
            dog = request.args.get('username')
            user = User.query.filter_by(username=dog).first()
            blogs = user.blog_posts
            if blogs == None:
                return render_template('user.html', user=user, blogs=blogs)
            return render_template('user.html', user=user, blogs=blogs)

            
        posts = Blog.query.all()
        return render_template('all-post.html', posts=posts)


@app.route('/', methods=['POST', 'GET'])
def display_users():

    if request.method == 'POST':
        username = request.form['username'] 

    else:
        dog = request.args.get('username')
        if dog:
            user = User.query.filter_by(username=dog).first()
            blogs = Blog.query.filter_by(owner=user).all()
            if blogs == None:
                return render_template('user.html', user=user, blogs=blogs)
            return render_template('user.html', user=user, blogs=blogs)
           
    users = User.query.all()
    return render_template('all-users.html', users=users)

def logged_in_user():
    owner = User.query.filter_by(username=session['user']).first()
    return owner

@app.before_request
def require_login():
    endpoints_without_login = ['login', 'register', 'display_users', 'display_posts']
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/login")

if __name__ == '__main__':
    app.run()