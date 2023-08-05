"""Imports required packages from flask and flask_sqlalchemy"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from data_models import Author, Book

# Create an instance of the Flask application
app = Flask(__name__)

# Setting the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/library.sqlite'

# Initialize the SQLAlchemy extension with the Flask application
db = SQLAlchemy()
db.init_app(app)

# Define a route and corresponding view function
@app.route('/')
def home():
    return 'Hello, World!'

if __name__ == '__main__':
    # Run the application in development mode
    app.run(host="0.0.0.0", port=5002, debug=True)
