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



#create a blog form
class BlogForm(Form):
    title = StringField('Title', [validators.DataRequired() ,validators.Length(min=6, max=120)])
    body = TextAreaField('Body', [validators.DataRequired(), validators.Length(min=20)])






@app.route('/')
def home():
    return render_template('home.html', title='Home')




if __name__ == '__main__':
    app.run(debug=True)