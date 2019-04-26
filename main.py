from flask import Flask, request, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from datetime import datetime
import myhelpers


#app configuration
app = Flask(__name__)
app.secret_key = 'NotSSOOs@cr@t_K&Y!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:BlogPassWord123@localhost:3306/buildablog'


#init db instance
db = SQLAlchemy(app)


#persistence data class for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    username = db.Column(db.String(60), unique=True)
    password = db.Column(db.String(120))
    #constructor   
    def __init__(self, username, password):
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



@app.route('/register')
def register():
    form = RegistrationForm(request.form)
    return render_template('register.html', title='Register', form=form)



@app.route('/login')
def login():
    form = LoginForm(request.form)
    return render_template('login.html', title='Login', form=form)



@app.route('/logout')
def logout():
    return render_template('logout.html', title='Logout')



@app.route('/blog_entry')
def blog_entry():
    form = BlogForm(request.form)
    return render_template('blog_entry.html', title='Blog Entry', form=form)




if __name__ == '__main__':
    app.run(debug=True)