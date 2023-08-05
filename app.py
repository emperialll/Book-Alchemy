"""Imports required packages from flask and flask_sqlalchemy"""
from flask import Flask, render_template, request
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
    return render_template('add_book.html')

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form.get('name')
        birth_date = request.form.get('birthdate')
        date_of_death = request.form.get('date_of_death')
        # data_manager.add_user(user_details)
        # return "Registration successful!"

    # Render the "add author" form template for GET requests
    return render_template('add_author.html')

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        # data_manager.add_user(user_details)
        return "The book has been added successfully!"

    # Render the "add book" form template for GET requests
    return render_template('add_book.html')

if __name__ == '__main__':
    # Run the application in development mode
    app.run(host="0.0.0.0", port=5002, debug=True)
