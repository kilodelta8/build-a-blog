from flask import Flask, request, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from datetime import datetime
from myhelpers import is_email


#app configuration
app = Flask(__name__)
app.secret_key = 'NotSSOOs@cr@t_K&Y!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:BlogPassWord123@localhost:3306/buildablog'
#app.config['SQLALCHEMY_ECHO'] = True

#init db instance
db = SQLAlchemy(app)


#persistence data class for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(120))
    #constructor   
    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password
    #represent son....
    def __repr__(self):
        return '<User %r>' % self.username

#persistence data class for Blogs
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
        nullable=False)
    #init a post
    def __init__(self, title, body):
        self.title = title
        self.body = body
    #reppin again....
    def __repr__(self):
        return (self.title, self.body)



#user registration form
class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=60)])
    email = StringField('Email', [validators.Length(min=6, max=120)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('verify', message='Passwords do not match')
    ])
    verify = PasswordField('Confirm Password')


#user login form
class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=60)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('verify', message='Passwords do not match')
    ])


#create a blog form
class BlogForm(Form):
    title = StringField('Title', [validators.DataRequired() ,validators.Length(min=6, max=120)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=20)])






@app.route('/')
def home():
    return render_template('home.html', title='Home')



@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        #fetch email and username to make sure the user isn't posing
        possibleEmail = User.query.filter_by(email=email).count()
        possibleUsername = User.query.filter_by(username=username).count()
        if not is_email(email):
            flash('Whoa! "' + email + '" does not seem like an email address!', 'danger')
            return redirect('/register')
        elif possibleEmail > 0:
            flash('Whoa! "' + email + '" is already in use!', 'danger')
            return redirect('/register')
        if possibleUsername > 0:
            flash('Whoa! "' + username + '" is already in use!', 'danger')
            return redirect('/register')
        if password != verify:
            flash('Whoa! "' + username + '"Passwords do not match!', 'danger')
            return redirect('/register')
        #if we made it this far and they pass the tests, lettuce add them.
        user = User(email, username, password)
        db.session.add(user)
        db.session.commit()
        return redirect('/')#maybe to a dashboard????????
    else:
        return render_template('register.html', title='Register', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username)
        if password == user.password:
            session['user'] = user.username
            flash('welcome back, '+ user.username)
            return redirect("/")
        flash('bad username or password')
        return redirect("/login")
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    del session['user']
    #return redirect("/")
    return render_template('logout.html', title='Logout')



@app.route('/blog_entry')
def blog_entry():
    form = BlogForm(request.form)
    return render_template('blog_entry.html', title='Blog Entry', form=form)


#list of permitted pages if not logged in session
endpoints_without_login = ['login', 'register', 'home']
#test before each route call to make sure user is in session
@app.before_request
def require_login():
    if not ('user' in session or request.endpoint in endpoints_without_login):
        return redirect("/register")




if __name__ == '__main__':
    app.run(debug=True)