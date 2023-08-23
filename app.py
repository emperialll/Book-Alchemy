"""Imports required packages from flask and flask_sqlalchemy"""
import os
import secrets
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
from datetime import datetime

# Create an instance of the Flask application
app = Flask(__name__)
# # Generate a secure random key
# secret_key = secrets.token_hex(16)  # Generates a 32-character hexadecimal key
# app.secret_key = secret_key

# Setting the database URI
db_path = os.path.abspath('data/library.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

# Initialize the SQLAlchemy extension with the Flask application
db = SQLAlchemy()
db.init_app(app)

# Define a route and corresponding view function


@app.route('/', methods=['GET', 'POST'])
def home():
    from data_models import Author, Book
    BOOK_COVER_API = 'https://covers.openlibrary.org/b/isbn/'

    if request.method == 'POST':
        query = request.form.get('query')
        if query:
            # Perform a search using the 'LIKE' operator with SQLAlchemy
            # Search for matches in book titles or author names
            books = Book.query.join(Author, Book.author_id == Author.id).add_columns(
                Book.title, Book.isbn, Book.publication_year, Author.name).filter(
                or_(Book.title.ilike(f"%{query}%"), Author.name.ilike(f"%{query}%"))).all()
            return render_template('home.html', books=books, api=BOOK_COVER_API)

    # Fetch all books and authors if no search query or GET request
    books = Book.query.join(Author, Book.author_id == Author.id).add_columns(
        Book.id, Book.title, Book.isbn, Book.publication_year, Book.author_id, Author.name).all()

    return render_template('home.html', books=books, api=BOOK_COVER_API)


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


@app.route('/book/<book_id>/delete', methods=['POST'])
def delete_book(book_id):
    from data_models import Author, Book
    try:
        book = Book.query.get(int(book_id))
        if book:
            author = Author.query.get(book.author_id)
            other_books_by_author = Book.query.filter_by(
                author_id=book.author_id).count()
            if other_books_by_author == 1:
                print("tooye if")
                author = db.session.merge(author)
                db.session.delete(author)
            book = db.session.merge(book)
            db.session.delete(book)
            db.session.commit()
            print('Book deleted successfully!')
            return redirect(url_for('home'))
        else:
            return 'Book not found.'

    except Exception as e:
        db.session.rollback()  # Rollback the transaction in case of an error
        print("Error:", str(e))
        return 'An error occurred while deleting the book.'


if __name__ == '__main__':
    # Run the application in development mode
    app.run(host="0.0.0.0", port=5002, debug=True)
