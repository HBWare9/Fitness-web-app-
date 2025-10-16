from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy import text  
import psycopg2
import os 
from flask import session 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.getenv("SECRET_KEY") or "some_fall_backkey"

db = SQLAlchemy(app)

class authTable(db.Model):
    __tablename__ = "auth"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        query = text("SELECT id FROM auth WHERE username = :username AND password = :password")
        with db.engine.connect() as dbconn:
            result = dbconn.execute(query, {"username": username, "password": password})
            row = result.fetchone()
            if row is not None: 
                session['uid'] = row[0]
                print(f"Login success with id {session.get('uid','0')}")
                return render_template('homepage.html')
            else: 
                return render_template('frontpage.html', error="Invalid login details, please try again")

    return render_template('frontpage.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_pass = request.form['passconfirm']
        
        if password == confirm_pass:
            
            query = text("INSERT INTO auth (username, password) VALUES (:username, :password)")

        
            with db.engine.connect() as dbconn:               
                dbconn.execute(query, {"username": username, "password": password})
                dbconn.commit()
            return redirect('/')
    else:
        return render_template("signup.html")


if __name__ == "__main__":
    app.run(debug=True)



    
    