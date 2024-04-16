from flask import Flask, render_template, redirect, request, url_for, session, flash
from flask_bootstrap import Bootstrap
import sqlite3


app = Flask(__name__)
app.secret_key = "ABC" #this is used to store the session in the server 
#bootstrap = Bootstrap(app)

#creating the table
@app.route('/')
def main() :
    con = sqlite3.connect('user.db')
    c   = con.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY AUTOINCREMENT,name TEXT, email TEXT, user_name TEXT, password TEXT)")
    con.commit()
    return redirect(url_for("index")) 
    
@app.route("/index")
def index():
    if "user" in session:
        return redirect(url_for("user"))
    return render_template("pages-login.html")

@app.route("/dashboard")
def dashboard():

    if "user" in session:
        user = session["user"]
        return render_template("index.html", user = user) 
    else:
        return redirect(url_for("login"))

    

#login page data pasing
@app.route("/login", methods = ["POST", "GET"])
def login():
    
    if request.method == "POST":
        
        user_name   = request.form["user_name"]
        password    = request.form["password"]
        con = sqlite3.connect('user.db')
        c   = con.cursor() 
        statement = f"SELECT * from user WHERE user_name = '{user_name}' AND password = '{password}'; "
        c.execute(statement)
        
        if not c.fetchone():
            #error message if password is incorrect
            flash(f'Incorrect User Name or Password!', 'error')
            
        else:
            session['user'] = user_name
            return redirect(url_for("user"))
        return redirect(url_for("login"))
    else:
        #if the user is already logged in then load the user page again
        
        if "user" in session:
            return redirect(url_for("user"))
        return render_template("pages-login.html")

#reg page data pasing
@app.route("/register", methods = ["POST", "GET"])
def register():
    con = sqlite3.connect('user.db')
    c   = con.cursor() 
    if request.method == "POST":
        name        = request.form["name"]
        email       = request.form["email"]
        user_name   = request.form["user_name"]
        password    = request.form["password"]
        
        #checking if the user is already in the db and show the error page
        statement = f"SELECT * from user WHERE user_name = '{user_name}' AND password = '{password}'; "
        c.execute(statement)
        data = c.fetchone()
        if data :
            return render_template("Error.html")
        else:
            if not data:
                statement = f"INSERT INTO user (name, email, user_name, password) VALUES ('{name}','{email}','{user_name}','{password}');"
                c.execute(statement)
                con.commit()
                con.close()
            return redirect(url_for("login"))
    
    else:    
        return render_template("pages-register.html")

#user login with a session
@app.route("/user")
def user():
   
    if "user" in session:
        user = session["user"]
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("login"))
    
@app.route("/profile")
def profile():

    if "user" in session:
        user = session["user"]

        con = sqlite3.connect('user.db')
        c = con.cursor()
        statement = f"SELECT * from user WHERE user_name = '{user}'; "
        c.execute(statement)
        user_data = c.fetchall()
        return render_template('users-profile.html', user_data = user_data)
    else:
        return redirect(url_for("login"))
    
    
    
#this is user to logout the session for the user
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))
    

if __name__=="__main__":
    app.run( debug=True)