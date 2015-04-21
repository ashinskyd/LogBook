"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask, request, redirect, render_template
from flask_login import (LoginManager, login_required, login_user, 
                         current_user, logout_user, UserMixin)
app = Flask(__name__)

wsgi_app = app.wsgi_app
form = LoginManager()
form.init_app(app)

class User():
    def __init__(self, userid, password):
        self.id = userid
        self.password = password

    @staticmethod
    def get(userid):

        #For this example the USERS database is a list consisting of 
        #(user,hased_password) of users.
        for user in USERS:
            if user[0] == userid:
                return User(user[0], user[1])
        return None

david = User("David","Ashinsky")
USERS = [david]
#print(User.get("David"))

@app.route('/')
def dataEntry():
    return render_template("DataEntry.html")


@app.route('/submit',methods=['POST'])
@login_required
def submit():
    hours  = request.form['hours']
    return render_template("DisplayData.html",hours=hours)


if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
