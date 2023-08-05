from sqlalchemy import Column, Date, ForeignKey, Integer, String
from app import app, db  # Import db instance from app.py

class Author(db.Model):
    """
    The "Author" Python class defines the authors table in the database.
    Database file: ../data/library.sqlite
    Columns: id (Primary Key), name, birth_date and date_of_death
    """
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    birth_date = Column(Date)
    date_of_death = Column(Date)

    def __repr__(self):
        return f"Author(id = {self.id}, name = {self.name})"
    def __str__(self):
        """
        Returns a human-readable string representation of the Author.

        Returns:
            str: A formatted string representing the Author's details.
        """
        birth_date_str = self.birth_date.strftime('%Y-%m-%d') \
            if self.birth_date else ''
        date_of_death_str = self.date_of_death.strftime('%Y-%m-%d') \
            if self.date_of_death else ''
        return f"Author ID: {self.id}\nName: \
            {self.name}\nBirth Date: {birth_date_str}\n\
                Date of Death: {date_of_death_str}"


class Book(db.Model):
    """
    The "Book" Python class defines the books table in the database.
    Columns: id (Primary Key), isbn, title, publication_year, 
    and author_id (Foreign Key to the Author table).
    """
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True, autoincrement=True)
    isbn = Column(String, nullable=False, unique=True)
    title = Column(String, nullable=False)
    publication_year = Column(Integer, nullable=False)
    author_id = Column(Integer, ForeignKey('authors.id'), nullable=False)

    def __repr__(self):
        """
        Returns the string representation of the Book object.

        Returns:
            str: A formatted string representing the Book object.
        """
        return f"Book(id={self.id}, title={self.title}"

    def __str__(self):
        """
        Returns a human-readable string representation of the Book.

        Returns:
            str: A formatted string representing the Book's details.
        """
        return f"Book ID: {self.id}\nISBN: {self.isbn}\n\
            Title: {self.title}\nPublication Year: {self.publication_year}\nA\
                uthor ID: {self.author_id}"

if __name__ == '__main__':
    # Create the new tables
    with app.app_context():
        db.create_all()
