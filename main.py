from flask import Flask, request, render_template, url_for, flash, redirect
import myhelpers

app = Flask(__name__)
app.secret_key = 'NotSSOOs@cr@t_K&Y!'



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