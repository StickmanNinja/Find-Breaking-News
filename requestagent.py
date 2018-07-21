from __future__ import print_function
# Importing flask.
from flask import Flask, render_template, url_for, session, redirect, request
from functions import *
import os
import sys
app = Flask(__name__)

# My own little version of console.log from JavaScript.
def consolelog(x):
    print (str(x), file=sys.stderr)

# Randomly generated key using os.urandom(24), saved to an environment variable.
app.secret_key = os.environ['BreakingNewsSecret']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True
@app.route('/login')
def login():
    session["user"] = "SethConnell"
    session["password"] = "sethconnell777"
    return "<h1>You are logged in!</h1>"

@app.route("/logintest")    
def login_test():
    if session["user"] == "SethConnell" and session["password"] == "sethconnell777":
        return "you did it!"
    else:
        return "error: You are not logged in!"
    
@app.route("/logout")
def logout():
    session.clear()
    if session.get("user") is None:
        return "<h1>You did it, boy!!</h1>"

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/success")
def success():
    return "<h1>Account created successfully!</h1>"

@app.route("/signup", methods = ["GET","POST"])
def signup():
    if request.method == 'POST':
        given_username = request.form["username"]
        given_password = request.form["password"]
        given_confirmpassword = request.form["confirmpassword"]
        if given_password == given_confirmpassword and checkUser(given_username) == True and checkString(given_username) == True and checkString(given_password) == True:
            consolelog(given_username)
            consolelog(given_password)
            createUser(given_username, given_password)
            return redirect(url_for('success'))
    else:
        return render_template("signup.html")
        
    



if __name__ == '__main__':
    app.run(debug=True)
