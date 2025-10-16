from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy 
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class authTable(db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    

if __name__ == "__main__":
    with app.app_context():
        user = authTable.query.first()
        if user:
            print(f"Found user: {user.username}")
        else:
            print("No users found in the table.")

    
    