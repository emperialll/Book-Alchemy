"""Imports required packages from flask and flask_sqlalchemy"""
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create an instance of the Flask application
app = Flask(__name__)

# Setting the database URI
db_path = os.path.abspath('data/library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Initialize the SQLAlchemy extension with the Flask application
db = SQLAlchemy()
db.init_app(app)

# Define a route and corresponding view function


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    from data_models import Author

    if request.method == 'POST':
        name = request.form.get('name')
        birth_date_str = request.form.get('birthdate')
        date_of_death_str = request.form.get('date_of_death')

        # Convert birth_date and date_of_death strings to Date objects
        birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        date_of_death = datetime.strptime(
            date_of_death_str, '%Y-%m-%d').date() if date_of_death_str else None

        # Create a new Author object with the form data
        new_author = Author(name=name, birth_date=birth_date,
                            date_of_death=date_of_death)

        # Add the Author to the database
        db.session.add(new_author)
        db.session.commit()

        return "The author has been added successfully!"

    # Render the "add author" form template for GET requests
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    from data_models import Author, Book

    # Fetch the list of authors from the database
    authors = Author.query.all()

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        publication_year = request.form.get('publication_year')
        author_id = request.form.get('author_id')
        # Create a new Book object with the form data
        new_book = Book(isbn=isbn, title=title,
                        publication_year=publication_year, author_id=author_id)

        # Add the Book to the database
        db.session.add(new_book)
        db.session.commit()

        return "The book has been added successfully!"

    # Render the "add book" form template for GET requests
    return render_template('add_book.html', authors=authors)


if __name__ == '__main__':
    # Run the application in development mode
    app.run(host="0.0.0.0", port=5002, debug=True)
