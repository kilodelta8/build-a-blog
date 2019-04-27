from flask import Flask, request, render_template, url_for, flash, redirect, session
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, PasswordField, TextAreaField, validators
from datetime import datetime


#app configuration
app = Flask(__name__)
app.secret_key = 'NotSSOOs@cr@t_K&Y!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://buildablog:BlogPassWord123@localhost:3306/buildablog'
app.config['SQLALCHEMY_ECHO'] = True

#init db instance
db = SQLAlchemy(app)



#persistence data class for Blogs
class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    #init a post
    def __init__(self, title, body):
        self.title = title
        self.body = body
    #reppin again....
    def __repr__(self):
        return (self.title, self.body)



#create a blog form
class BlogForm(Form):
    title = StringField('Title', [validators.Length(min=6, max=120)])
    body = TextAreaField('Body', [validators.Length(min=20)])




#display a single blog post by ID query
@app.route('/blog/<int:id>/', methods=['GET', 'POST'])
def blog(id):
    blog = Blog.query.get(id)
    return render_template('blog.html', title=blog.title, blog=blog)



#create a new blog post with error checking
@app.route('/newpost', methods=['GET', 'POST'])
def newpost():
    form = BlogForm(request.form)
    if request.method == 'POST':
        title = request.form['title'] 
        body = request.form['body']
        if len(title) < 1:
            flash('You must add a title!', 'danger')
            redirect(url_for('newpost'))
        elif len(body) < 1:
            flash('You must provide content to the body!', 'danger')
            redirect(url_for('newpost'))
        else:
            blog = Blog(title, body)
            db.session.add(blog)
            db.session.commit()
            last_item = Blog.query.order_by(Blog.id.desc()).first()
            id = last_item.id
            return render_template('blog.html', blog=blog)
    return render_template('newpost.html', title='Add and Entry', form=form)


#home route displaying all blogs in the db
@app.route('/')
def home():
    blog = Blog.query.order_by(Blog.pub_date.desc()).all()
    return render_template('home.html', title='Home', blogs=blog)




#Non-prodution
if __name__ == '__main__':
    app.run(debug=True)