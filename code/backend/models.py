from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime, timedelta
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role = Column(Text, nullable=False) # admin or user
    joined_date = Column(DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    book_requests = relationship('BookRequest', back_populates='user', cascade='all, delete-orphan')
    feedback = relationship('Feedback', back_populates='user', cascade='all, delete-orphan')
    

    def __init__(self, name, email, password, role, joined_date=None):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.joined_date = joined_date

class Section(db.Model):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    description = Column(Text, nullable=True)
    books = relationship('Book', back_populates='section', cascade='all, delete-orphan')

    def __init__(self, name, description, date_created=None):
        self.name = name
        self.description = description
        self.date_created = date_created 

class Book(db.Model):
    __tablename__ = 'book'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    content = Column(Text, nullable=True)
    author = Column(Text, nullable=False)
    date_created = Column(DateTime, default=datetime.utcnow)
    
    image = Column(Text, nullable=True) 

    section_id = Column(Integer, ForeignKey('section.id'), nullable=False)
    section = relationship('Section', back_populates='books')
    book_requests = relationship('BookRequest', back_populates='book', cascade='all, delete-orphan')
    feedback = relationship('Feedback', back_populates='book', cascade='all, delete-orphan')


    def __init__(self, name, section_id, author, content=None, date_created=None, image=None):
        self.name = name
        self.section_id = section_id
        self.content = content
        self.author = author
        self.date_created = date_created
        
        self.image = image

class BookRequest(db.Model):
    __tablename__ = 'book_request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_name = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    book_name = Column(Text, nullable=False)
    request_date = Column(DateTime, default=datetime.utcnow)
    return_date = Column(DateTime, nullable=True, default=datetime.utcnow() + timedelta(days=7))
    status = Column(Text, nullable=False, default='pending')  # pending, accepted, rejected, revoked

    user = relationship('User', back_populates='book_requests')
    book = relationship('Book', back_populates='book_requests')

    def __init__(self, user_id, user_name, book_id, book_name, request_date, return_date, status):
        self.user_id = user_id
        self.user_name = user_name
        self.book_id = book_id
        self.book_name = book_name
        self.request_date = request_date
        self.return_date = return_date
        self.status = status

class BookRequestSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "user_name", "book_id", "book_name", "request_date", "return_date", "status")

request_schema = BookRequestSchema()
requests_schema = BookRequestSchema(many=True)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "role", "joined_date")

userschema = UserSchema()
usersschema = UserSchema(many=True)

class SectionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'description', 'date_created')

sectionschema = SectionSchema()
sectionsschema = SectionSchema(many=True)

class BookSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'section_id', 'content', 'author', 'date_created', 'image')  # Include image field

bookschema = BookSchema()
booksschema = BookSchema(many=True)

class DeletedRequest(db.Model):
    __tablename__ = 'deleted_request'
    id = Column(Integer, primary_key=True, autoincrement=True)
    request_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    user_name = Column(Text, nullable=False)
    book_id = Column(Integer, nullable=False)
    book_name = Column(Text, nullable=False)
    request_date = Column(DateTime, nullable=False)
    status = Column(Text, nullable=False)
    deleted_date = Column(DateTime, default=datetime.utcnow)

class DeletedRequestSchema(ma.Schema):
    class Meta:
        fields = ("id", "request_id", "user_id", "user_name", "book_id", "book_name", "request_date", "status", "deleted_date")

deleted_request_schema = DeletedRequestSchema()
deleted_requests_schema = DeletedRequestSchema(many=True)

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user_name = Column(Text, nullable=False)
    book_id = Column(Integer, ForeignKey('book.id'), nullable=False)
    book_name = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    feedback_date = Column(DateTime, default=datetime.utcnow)

    user = relationship('User', back_populates='feedback')
    book = relationship('Book', back_populates='feedback')

    def __init__(self, user_id, user_name, book_id, book_name, rating, comment, feedback_date):
        self.user_id = user_id
        self.user_name = user_name
        self.book_id = book_id
        self.book_name = book_name
        self.rating = rating
        self.comment = comment
        self.feedback_date = feedback_date

class FeedbackSchema(ma.Schema):
    class Meta:
        fields = ("id", "user_id", "user_name", "book_id", "book_name", "rating", "comment", "feedback_date")

feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)
