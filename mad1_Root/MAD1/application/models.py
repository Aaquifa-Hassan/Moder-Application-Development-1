from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(50),unique = True,nullable = False)
    password = db.Column(db.String(255), nullable=False)
    lendedBooks = db.Column(db.Integer)
    role = db.Column(db.String(50), nullable=False)
    lended_books = db.relationship('BookLended', backref='user', lazy=True)

class Section(db.Model):
    section_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    description = db.Column(db.Text)

class Book(db.Model):
    book_id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey('section.section_id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(200), nullable=False)
    date_issued = db.Column(db.Date)
    return_date = db.Column(db.Integer)
    price = db.Column(db.Float, nullable=False)
    section = db.relationship('Section', backref=db.backref('books', lazy=True))

class BookRequest(db.Model):
    request_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    request_date = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    user = db.relationship('User', backref=db.backref('book_requests', lazy=True))
    book = db.relationship('Book', backref=db.backref('requests', lazy=True))

class BookLended(db.Model):
    lend_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    lend_date = db.Column(db.DateTime, nullable=False, default=datetime.now().date())
    return_date = db.Column(db.DateTime)
    book = db.relationship('Book', backref=db.backref('lended_books', lazy=True))

class Feedback(db.Model):
    feedback_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    feedback_text = db.Column(db.Text, nullable=False)
    user = db.relationship('User', backref=db.backref('feedbacks', lazy=True))
    book = db.relationship('Book', backref=db.backref('feedbacks', lazy=True))

class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.book_id'), nullable=False)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.now().date())
    price = db.Column(db.Float, nullable=False)
