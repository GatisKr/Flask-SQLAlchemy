from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create an instance of the SQLAlchemy class

class Post(db.Model):  # Define a class 'Post' that inherits from SQLAlchemy Model class
    # Define columns for rhe 'Post' table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for unique identification
    title = db.Column(db.String(300), nullable=False)  # Column for the post title, not nullable (can not be empty)
    text = db.Column(db.Text, nullable=False)  # Column for the post content

class User(db.Model):  # Define a class 'User' that inherits the SQLAlchemy Model class
    # Define columns for the 'Person' table
    id = db.Column(db.Integer, primary_key=True)  # Primary key column for unique identification
    name = db.Column(db.String(300), nullable=False)  # Column for the user's name
    password = db.Column(db.String(300), nullable=False)  # Column for user's password
    age = db.Column(db.Integer, nullable=False)  # Column for the person's age
    isAdmin = db.Column(db.Boolean, nullable=False)  # Is user admin

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    messageText = db.Column(db.String(300), nullable=False)
    priority = db.Column(db.Integer, nullable=False)
