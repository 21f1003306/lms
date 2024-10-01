from flask import Flask, request, jsonify, send_file, send_from_directory, Response
from models import *
from config import Config
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from flask_cors import CORS
from datetime import datetime
import os 
from worker import celery_init_app
from celery.schedules import crontab
import task
from cache import cache
import io
from io import StringIO
import csv



class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'veryyysecret'

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)

app.config["CELERY"] = {
    "broker_url": "redis://localhost:6379/0",
    "result_backend": "redis://localhost:6379/0",
}
celery = celery_init_app(app)

db.init_app(app)
ma.init_app(app)
bcrypt = Bcrypt(app)
with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True)

cache.init_app(app)

# Home Page
@app.route("/")
def hello():
    return "Hello, World! This is my home page"

# Register Page
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    name = data.get('name')
    role = data.get('role')

    existing_user = User.query.filter_by(name=name).first()  
    if existing_user:
        return jsonify({"error": "User with this name already exists"}), 409

    existing_email = User.query.filter_by(email=email).first()  
    if existing_email:
        return jsonify({"error": "User with this email already exists"}), 409

    if role == "admin":
        existing_admin = User.query.filter_by(role="admin").first()  
        if existing_admin:
            return jsonify({"error": "An admin user already exists"}), 409
        else:
            # Register the user as admin
            new_user = User(name=name, email=email, password=password, role=role)
            try:
                db.session.add(new_user)
                print("New admin user added to the session:", new_user)  # Debugging statement
                db.session.commit()
                print("New admin user committed to the database:", new_user)  # Debugging statement
                return jsonify({"message": "Admin user created successfully"}), 201
            except Exception as e:
                db.session.rollback()
                print("Error creating admin user:", e)  # Debugging statement
                return jsonify({"error": "Error creating admin user"}), 500
        
    new_user = User(name=name, email=email, password=password, role=role)

    try: 
        db.session.add(new_user)
        print("New user added to the session:", new_user)  # Debugging statement
        db.session.commit()
        print("New user committed to the database:", new_user)  # Debugging statement
        if role == "user":
            return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print("Error creating user:", e)  # Debugging statement
        return jsonify({"error": "Error creating user"}), 500


#Login Page
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    
    # Fetch the user by email and role
    user = User.query.filter_by(email=email, role=role).first()

    if not user:
        return jsonify({"error": "User not found, register first"}), 404

    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 401

    # Update last_login time with the current time
    user.last_login = datetime.utcnow()
    db.session.commit()

    # Create a new JWT access token
    access_token = create_access_token(identity={
        'id': user.id,
        'role': user.role,
    })

    return jsonify({"message": "Login successful", "access_token": access_token}), 200

#User Protection
@app.route("/protected")
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "This route is very protected. You don't have authorization to access it."}), 401
    return jsonify({"message": "Hi Admin"}), 200

#Logout Page
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

#Getting User
@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def getuserinfo():
    this_user = get_jwt_identity()
    user = User.query.get(this_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = userschema.dump(user)
    return jsonify(user_data), 200

# Get All Users
@app.route('/all-users', methods=['GET'])
# @jwt_required()
def get_all_users():
    users = User.query.all()
    users_data = [{
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'role': user.role,
        'joined_date': user.joined_date.strftime('%Y-%m-%d') if user.joined_date else None
    } for user in users]
    return jsonify(users_data), 200

# Delete User
@app.route('/delete-user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

# CREATE Section
@app.route('/section', methods=['POST'])
@jwt_required()
def create_section():
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Very Protected Route, You don't have auth"}), 401
    data = request.json
    name = data.get('name')
    description = data.get('description') 
    if not name:
        return jsonify({"error": "Name is required for the section"}), 400

    existing_section = Section.query.filter_by(name=name).first()
    if existing_section:
        return jsonify({"error": "Section already exists"}), 409
    
    new_section = Section(name=name, description=description)  # Add description parameter here

    try:
        db.session.add(new_section)
        db.session.commit()
        return jsonify({"message": "Section created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating section"}), 500


# READ Section
@app.route('/section/<int:id>', methods=['GET'])
def get_section(id):
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    return jsonify({"section_data":sectionschema.dump(section)}), 200

# UPDATE Section
@app.route('/section/<int:id>', methods=['PUT'])
@jwt_required()
def update_section(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Unauthorized. You don't have permission to access this resource."}), 401
    
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    
    data = request.json
    section.name = data.get('name', section.name)  # Use existing name if not provided
    section.description = data.get('description', section.description)  # Use existing description if not provided

    db.session.commit()
    return jsonify({"message": "Section updated successfully"}), 200


#Delete Section
@app.route('/section/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_section(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    section = Section.query.get(id)
    if not section:
        return jsonify({"error": "Section not found"}), 404
    db.session.delete(section)
    db.session.commit()
    return jsonify({"message": "Section deleted successfully"}), 200

# Read all sections
@app.route('/sections', methods=['GET'])
def get_sections():
    sections = Section.query.all()
    return jsonify({"sections":sectionsschema.dump(sections)}), 200



#Create book
# API to create a Books in a Section (can be done by admin)
@app.route('/section/<int:section_id>/add-book', methods=['POST'])
@jwt_required()
def add_book_to_section(section_id):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] != "admin":
            return jsonify({"error": "Very Protected Route, You don't have auth"}), 401
        
        # Handle form data and file upload
        book_name = request.form.get('name')
        book_content = request.files.get('book_content')
        book_author = request.form.get('author')
        book_image = request.files.get('book_image')  # Get the file from the request
        print(type(book_image))
        print(type(book_content))
        if not book_name or not book_author:
            return jsonify({'message': 'Missing required fields (name, author)'}), 400
        new_book = Book(
            name=book_name,
            #content=book_content,
            author=book_author,
            section_id=section_id,
        )

        db.session.add(new_book)
        db.session.flush()
        book_id = new_book.id
        # Save the uploaded image
        if book_image:
            filename = f"{book_id}.png"  # Generate a unique filename
            image_path = os.path.join('static/', filename)
            book_image.save(image_path)
            new_book.image = filename
        else:
            new_book.image = None

        if book_content:
            fname = f"{book_id}.pdf" # Generate a unique filename
            content_path = os.path.join('uploads/', fname)
            book_content.save(content_path)
            new_book.content = fname
        else:
            new_book.content = None        

        db.session.commit()
        return jsonify({'message': 'Book added to section successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# GET ALL BOOKS IN A SECTION

@app.route('/books', methods=['GET'])
#@cache.cached(10)
def view_all_books():
    # Cache the result for 10 seconds
    print("Not cached")
    try:
        all_books = Book.query.all()
        print(all_books)
        if not all_books:    
            return jsonify({'message': 'No books found.'}), 404
        books_data = booksschema.dump(all_books)
        return jsonify({'books': books_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching books: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500

#GET SINGLE BOOK
@app.route('/book/<int:book_id>', methods=['GET'])
def view_book(book_id):
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404   
        book_data = bookschema.dump(book)
        section = Section.query.get(book.section_id)
        return jsonify({'book': book_data, "section_name": section.name}), 200
    except Exception as e:
        print(f"Error occurred while fetching book details: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500

#Update Book
@app.route('/book/<int:book_id>', methods=['PUT'])
@jwt_required()
def update_book(book_id):
    try:
        current_user = get_jwt_identity()
        if current_user['role'] != "admin":
            return jsonify({'error': 'Page Restricted!'}), 401

        book = Book.query.get(book_id)
        if not book:
            return jsonify({'message': 'Book not found'}), 404

        data = request.json
        book.name = data.get('name', book.name)
        book.content = data.get('content', book.content)
        book.author = data.get('author', book.author)

        db.session.commit()

        return jsonify({'message': 'Book updated successfully'}), 200

    except Exception as e:
        print(f"Error occurred while updating book: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500
    
#View Books by Section
@app.route('/section/<int:section_id>/books', methods=['GET'])
def view_books_by_section(section_id):
    try:
        books = Book.query.filter_by(section_id=section_id).all()
        if not books:
            return jsonify({'message': 'No books found in this section'}), 404
        books_data = booksschema.dump(books)
        return jsonify({'books': books_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching books: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500



# Delete a book
@app.route('/book/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_book(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Very Protected Route, You don't have authorization"}), 401
    
    book = Book.query.get(id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    
    try:
        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error deleting book"}), 500

from flask import send_from_directory
@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    return send_from_directory('static/', filename)

@app.route('/content/<int:id>', methods=['GET'])
def get_content(id):
    book=Book.query.filter_by(id=id).first()
    filename=book.content
    return send_from_directory('uploads/',filename )    



# Book Request by User
@app.route('/request-book', methods=['POST'])
# @jwt_required()
def request_book():
    data = request.get_json()
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    book_id = data.get('book_id')
    book_name = data.get('book_name')
    
    new_request = BookRequest(user_id=user_id, user_name=user_name, book_id=book_id, book_name=book_name, request_date=datetime.utcnow(), return_date=datetime.utcnow() + timedelta(days=7), status='pending')
    # User can make at most 5 requests
    if BookRequest.query.filter_by(user_id=user_id).count() >= 5:
        return jsonify({"message": "You can make at most 5 requests"}), 400

    db.session.add(new_request)
    db.session.commit()

    return jsonify({"message": "Book request created successfully"}), 201

@app.route('/requests', methods=['GET'])
@jwt_required()
def get_requests():
    current_user = get_jwt_identity()
    requests = BookRequest.query.filter_by(user_id=current_user['id']).all()
    requests_data = []
    for request in requests:
        book = Book.query.get(request.book_id)
        requests_data.append({
            'id': request.id,
            'user_id': request.user_id,
            'user_name': request.user_name,
            'book_id': request.book_id,
            'book_name': request.book_name,
            'request_date': request.request_date,
            'return_date': request.return_date,
            'status': request.status,
        })
    return jsonify({'requests': requests_data}), 200


@app.route('/user-requests', methods=['GET'])
def get_user_requests():
    # user_id = request.args.get('user_id')
    requests = BookRequest.query.all()
    requests_data = []
    for request in requests:
        book = Book.query.get(request.book_id)
        requests_data.append({
            'id': request.id,
            'user_id': request.user_id,
            'user_name': request.user_name,
            'book_id': request.book_id,
            'book_name': request.book_name,
            'request_date': request.request_date,
            'return_date': request.return_date,
            'status': request.status,
        })
    return jsonify({'requests': requests_data}), 200

# Accept Request
# admin can accept request and the status in database will get change to "accepted"
@app.route('/accept-request', methods=['POST'])
# @jwt_required()
def accept_request():
    from flask import request
    data = request.json
    request_id = data.get('request_id')
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"message": "Request not found"}), 404
    request.status = 'accepted'
    request.request_date = datetime.utcnow()
    request.return_date = datetime.utcnow() + timedelta(days=7)
    print('new date', request.return_date)
    db.session.commit()
    from task import send_email_task
    # send email to user
    send_email_task.delay(request.user.email, request.book_name)

    return jsonify({"message": "Request accepted successfully"}), 200

# Return Book
# user can return the book and the status in database will get change to "returned"
@app.route('/return-book', methods=['POST'])
@jwt_required()  # Ensure authentication is required
def return_book():
    current_user = get_jwt_identity()
    data = request.json
    request_id = data.get('request_id')
    book_request = BookRequest.query.filter_by(id=request_id, user_id=current_user['id']).first()

    if not book_request:
        return jsonify({"message": "Request not found"}), 404

    book_request.status = 'returned'
    db.session.commit()
    return jsonify({"message": "Book returned successfully"}), 200

# Reject Request
# admin can reject request and the status in database will get change to "rejected"
@app.route('/reject-request', methods=['POST'])
# @jwt_required()
def reject_request():
    from flask import request
    data = request.json
    request_id = data.get('request_id')
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"message": "Request not found"}), 404
    request.status = 'rejected'
    db.session.commit()
    return jsonify({"message": "Request rejected successfully"}), 200

# Revoke Request
# admin can revoke the book or the book can revoked automatically for which the request status is "accepted" and return_date is less than current date
# when admin revoke the book then the status in database will get change to "revoked" 
@app.route('/revoke-request', methods=['POST'])
# @jwt_required()
def revoke_request():
    from flask import request
    data = request.json
    request_id = data.get('request_id')
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"message": "Request not found"}), 404
    if request.status == 'accepted' or  request.return_date < datetime.utcnow():
        request.status = 'revoked'
        db.session.commit()
        return jsonify({"message": "Book revoked successfully"}), 200
    else:
        return jsonify({"message": "Book cannot be revoked"}), 400
        
# Delete Request
# admin can delete the request from the database if the status is "revoked" or "rejected"
@app.route('/delete-request', methods=['POST'])
def delete_request():
    from flask import request
    data = request.json
    request_id = data.get('request_id')
    request = BookRequest.query.get(request_id)
    if not request:
        return jsonify({"message": "Request not found"}), 404
    if request.status == 'revoked' or request.status == 'rejected' or request.status == 'returned':
        deleted_request = DeletedRequest(
            request_id=request.id,
            user_id=request.user_id,
            user_name=request.user_name,
            book_id=request.book_id,
            book_name=request.book_name,
            request_date=request.request_date,
            status=request.status
        )
        db.session.add(deleted_request)
        db.session.delete(request)
        db.session.commit()
        return jsonify({"message": "Request deleted successfully"}), 200
    else:
        return jsonify({"message": "Request cannot be deleted"}), 400



from flask import jsonify
from sqlalchemy import func

@app.route('/admin/stats', methods=['GET'])
# @jwt_required()  # Uncomment this if you're using JWT for authentication
def get_admin_stats():
    # Total number of users
    total_users = User.query.count() - 1  # Exclude the admin user

    # Total number of books
    total_books = Book.query.count()

    # Total number of sections
    total_sections = Section.query.count()

    # Total number of pending requests
    pending_requests = BookRequest.query.filter_by(status='pending').count()

    # Total number of accepted requests
    accepted_requests = BookRequest.query.filter_by(status='accepted').count()

    # Total number of rejected requests
    rejected_requests = BookRequest.query.filter_by(status='rejected').count()

    # Total number of revoked requests
    revoked_requests = BookRequest.query.filter_by(status='revoked').count()

    # Total number of deleted requests
    deleted_requests = DeletedRequest.query.count()
    # Most requested book
    most_requested_book = db.session.query(
        BookRequest.book_name, func.count(BookRequest.book_id).label('count')
    ).group_by(BookRequest.book_name).order_by(func.count(BookRequest.book_id).desc()).first()

    most_requested_book_name = most_requested_book[0] if most_requested_book else None
    most_requested_book_count = most_requested_book[1] if most_requested_book else 0

    stats = {
        'total_users': total_users,
        'total_books': total_books,
        'total_sections': total_sections,
        'pending_requests': pending_requests,
        'accepted_requests': accepted_requests,
        'rejected_requests': rejected_requests,
        'revoked_requests': revoked_requests,
        'deleted_requests': deleted_requests,
        'most_requested_book_name': most_requested_book_name,
        'most_requested_book_count': most_requested_book_count
    }

    return jsonify(stats), 200

@app.route('/user/stats', methods=['GET'])
@jwt_required()
def get_user_stats():
    current_user = get_jwt_identity()
    user_id = current_user['id']
    
    # Total books requested by the user
    total_requested = BookRequest.query.filter_by(user_id=user_id).count()
    
    # Total books accepted for the user
    total_accepted = BookRequest.query.filter_by(user_id=user_id, status='accepted').count()
    
    # Total books read/returned by the user (assuming 'read' or 'returned' status exists)
    total_read = BookRequest.query.filter_by(user_id=user_id, status='returned').count()

    stats = {
        'total_requested': total_requested,
        'total_accepted': total_accepted,
        'total_read': total_read
    }

    return jsonify(stats), 200

@app.route('/mybooks', methods=['GET'])
@jwt_required()
def get_my_books():
    current_user = get_jwt_identity()
    accepted_requests = BookRequest.query.filter_by(user_id=current_user['id'], status='accepted').all()
    
    if not accepted_requests:
        return jsonify({"message": "No accepted books found"}), 404

    books_data = []
    for request in accepted_requests:
        book = Book.query.get(request.book_id)
        if book:
            books_data.append({
                'request_id': request.id,
                'book_id': book.id,
                'book_name': book.name,
                'author': book.author,
                'date_requested': request.request_date
            })
    
    return jsonify(books_data), 200

# Submit feedback route
@app.route('/submit-feedback', methods=['POST'])
# @jwt_required()
def submit_feedback():
    data = request.get_json()
    user_id = data.get('user_id')
    user_name = data.get('user_name')
    book_id = data.get('book_id')
    book_name = data.get('book_name')
    rating = data.get('rating')
    comment = data.get('comment')

    new_feedback = Feedback(user_id=user_id, user_name=user_name, book_id=book_id, book_name=book_name, rating=rating, comment=comment, feedback_date=datetime.utcnow())
    existing_feedback = Feedback.query.filter_by(user_id=user_id, book_id=book_id).first()
    if existing_feedback:
        return jsonify({"message": "Feedback already exists for this book."}), 400
    # Add feedback to database  
    db.session.add(new_feedback)
    db.session.commit()

    return jsonify({'message': 'Feedback submitted successfully'}), 201

# get feedbacks method for my-feedback route
@app.route('/my-feedbacks', methods=['GET'])
@jwt_required() 
def get_my_feedback():
    current_user = get_jwt_identity()
    user_id = current_user['id']
    feedbacks = Feedback.query.filter_by(user_id=user_id).all()

    feedbacks_data = []
    for feedback in feedbacks:
        book = Book.query.get(feedback.book_id)
        feedbacks_data.append({
            'id': feedback.id,
            'user_id': feedback.user_id,
            'user_name': feedback.user_name,
            'book_id': feedback.book_id,
            'book_name': feedback.book_name,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'feedback_date': feedback.feedback_date
        })

    return jsonify(feedbacks_data), 200

# get feedbacks method for admin-feedback route
@app.route('/admin-feedback', methods=['GET'])
@jwt_required()
def get_admin_feedback():
    feedbacks = Feedback.query.all()

    feedbacks_data = []
    for feedback in feedbacks:
        book = Book.query.get(feedback.book_id)
        feedbacks_data.append({
            'id': feedback.id,
            'user_id': feedback.user_id,
            'user_name': feedback.user_name,
            'book_id': feedback.book_id,
            'book_name': feedback.book_name,
            'rating': feedback.rating,
            'comment': feedback.comment,
            'feedback_date': feedback.feedback_date
        })

    return jsonify(feedbacks_data), 200

# most recently added book which gets recently added books on the basis of date created
@app.route('/most-recent-books', methods=['GET'])
def get_most_recent_books():
    # Query the most recent 3 books in ascending order by date_created
    books = Book.query.order_by(Book.date_created.desc()).limit(3).all()
    
    # Convert the list of Book objects to a list of dictionaries
    book_list = [
        {
            'id': book.id,
            'name': book.name,
            'section': book.section.name,
            'section_id': book.section_id,
            'content': book.content,
            'image': book.image,
            'author': book.author,
            'date_created': book.date_created.isoformat()  # Convert datetime to ISO format
        }
        for book in books
    ]
    
    return jsonify(book_list)

# Update profile route
@app.route('/update-profile/<int:id>', methods=['PUT'])
@jwt_required()
def update_profile(id):
    current_user = get_jwt_identity()
    user = User.query.get(current_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    data = request.json
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.role = data.get('role', user.role)
    
    db.session.commit()
    return jsonify({'message': 'Profile updated successfully'})

@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Runs every minute
    sender.add_periodic_task(
        crontab(minute="*"),  
        task.daily_reminder.s(),
        name='daily_reminder'
    )
    # Runs every 2 minutes
    sender.add_periodic_task(
        crontab(minute='*/2'),  
        task.monthly_report.s(),
        name='monthly_report'
    )
    # Runs every 3 minutes
    sender.add_periodic_task(
        crontab(minute='*/1'),
        task.book_return_alert.s(),
        name='book_return_alert'
    )
    
# export csv route to admin
def generate_book_request_export_csv():
    # Query only requests with status 'accepted'
    requests = BookRequest.query.filter_by(status='accepted').all()
    
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['User Name', 'Book Name', 'Status', 'Request Date', 'Return Date'])

    for request in requests:
        csv_writer.writerow([request.user_name, request.book_name, request.status, request.request_date.strftime('%Y-%m-%d'), request.return_date.strftime('%Y-%m-%d')])

    csv_buffer.seek(0)
    return csv_buffer.getvalue()

@app.route('/download-book-requests', methods=['GET'])
def download_book_request_export_csv():
    csv_data = generate_book_request_export_csv()
    return Response(
        csv_data,
        mimetype='text/csv',
        headers={'Content-Disposition': 'attachment;filename=book_request_export.csv'}
    )

# caching example
@app.route('/greet/<string:name>')
@cache.cached(10)
def greet(name):
    print(name)
    return "Hello, " + name

if __name__ == "__main__":
    app.run(debug=True)
 