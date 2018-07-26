from __future__ import print_function
# Importing flask.
from flask import Flask, render_template, url_for, session, redirect, request
from functions import *
from MinimalTrello import *
import os
import sys
app = Flask(__name__)

# My own little version of console.log from JavaScript.
def consolelog(x):
    print (str(x), file=sys.stderr)

# Randomly generated key using os.urandom(24), saved to an environment variable.
app.secret_key = os.environ['BreakingNewsSecret']
app.config['TRAP_BAD_REQUEST_ERRORS'] = True

@app.route('/login', methods = ["GET","POST"])
def login():
    if request.method == 'POST':
        given_username = request.form["username"]
        given_password = request.form["password"]
        if lookupUser(given_username, given_password) == True:
            session["user"] = given_username
            return redirect(url_for('success'))
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    if session.get("user") is None:
        return "<h1>You did it, boy!!</h1>"

@app.route("/JSON")
def JSON():
    return "JSON Example."

@app.route("/trello")
def trello():
    if lookupToken(session["user"]) == True:
        return "You already gave us your trello token!"
    else:
        return render_template("trello_notoken")

@app.route("/submittrellotoken", methods = ["GET","POST"])
def submission():
    global key
    global token
    if request.method == 'POST':
        token = request.form["trellotoken"]
        if Trello(key, token).checkToken(token) == True:
            addToken(session["user"], token)
            return "Token Added Successfully!"
        else:
            return "Uh oh. That's not a valid token!"

@app.route("/email")
def email():
    return "Email Example."

@app.route('/')
@app.route('/home')
def home():
    return render_template('index.html')

@app.route("/success")
def success():
    return render_template("panel.html", user=session["user"])

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
            session["user"] = given_username
            return redirect(url_for('success'))
    else:
        return render_template("signup.html")
        
    



if __name__ == '__main__':
    app.run(debug=True)
