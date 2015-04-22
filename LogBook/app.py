"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, redirect, render_template, flash,url_for,g
from flask_login import (LoginManager, login_required, login_user, 
                         current_user, logout_user, UserMixin)
import redis
from datetime import timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SET T0 4NY SECRET KEY L1KE RAND0M H4SH'
wsgi_app = app.wsgi_app
app.permanent_session_lifetime = timedelta(seconds=10)

login_manager = LoginManager()
login_manager.init_app(app)

class UserNotFoundError(Exception):
    pass


class User(UserMixin):
    USERS = {
        'a': 'b'}

    def __init__(self, id):
        if not id in self.USERS:
            raise UserNotFoundError()
        self.id = id
        self.password = self.USERS[id]
    def get_id(self):
        return str(self.id)
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def is_authenticated(self):
        return True   
    @classmethod
    def get(self_class, id):
        '''Return user instance of id, return None if not exist'''
        try:
            return self_class(id)
        except UserNotFoundError:
            return None

@login_manager.user_loader
def load_user(userid):
    return User.get(userid)

@app.route('/',methods=['GET','POST'])
def index():
    return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
    if (current_user):
        return "AAA"
    elif request.method == 'GET':
        return render_template("Login.html")
    else:
        username = request.form['username']
        password = request.form['password']
        u = User.get(username)
        if (u and u.password == password):
            login_user(u,remember=True)
            u.authenticated = True
            return redirect(url_for('dataEntry'))
        else:
            return render_template("Login.html",error=True)

@app.route('/dataEntry',methods=['GET'])
@login_required
def dataEntry():
    return render_template("DataEntry.html")

@app.route('/displayData',methods=['POST'])
@login_required
def displayData():
    hours  = request.form['hours']
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    oldval = r.get('hours')
    if oldval is None:
        r.set('hours',hours) 
    else:
        r.set('hours',hours+oldval)
    return render_template("DisplayData.html",hours=r.get('hours'))

@app.route('/logout',methods=['GET'])
@login_required
def logout():
    user = current_user
    user.authenticated=False
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
