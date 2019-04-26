from flask import Flask, request, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
import myhelpers


#app configuration
app = Flask(__name__)
app.secret_key = 'NotSSOOs@cr@t_K&Y!'
#TODO - need to build the db still yet
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://flicklist:MyNewPass@localhost:3306/flicklist'


#init db instance
#db = SQLAlchemy(app)






@app.route('/')
def home():
    return render_template('home.html', title='Home')



@app.route('/register')
def register():
    return render_template('register.html', title='Register')



@app.route('/login')
def login():
    return render_template('login.html', title='Login')



@app.route('/logout')
def logout():
    return render_template('logout.html', title='Logout')




if __name__ == '__main__':
    app.run(debug=True)