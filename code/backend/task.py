from celery import shared_task
from flask import current_app
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template
import time
import os
from flask_mail import Mail, Message
from models import User, BookRequest, db, Feedback 
from datetime import datetime, timedelta
from flask import render_template


# Task to send daily reminder email to user whose last login was less than 1 minute ago
@shared_task
def daily_reminder():
    threshold = datetime.utcnow() - timedelta(days=1)
    users_to_remind = User.query.filter(User.last_login < threshold).all()

    smtp_obj = smtplib.SMTP('localhost', 1025)

    with open("./templates/daily_reminder.html") as file:
        content = Template(file.read())

    for user in users_to_remind:
        msg = MIMEMultipart()
        msg['Subject'] = "Daily Reminder"
        msg['From'] = "a@admin.com"
        msg['To'] = user.email

        html = MIMEText(content.render(username=user.name), 'html')
        msg.attach(html)

        smtp_obj.sendmail("a@admin.com", user.email, msg.as_string())

    smtp_obj.quit()

# Task to send email to user whose book request has been accepted
@shared_task
def send_email_task(user_email, book_name):
    
    subject = 'Book Request Accepted'
    html_body = f"""
    <html>
    <body>
        <p>Your request for the book <strong>{book_name}</strong> has been accepted.</p>
        <p>Please read the book</p>
    </body>
    </html>
    """

    # Create the email message
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "Book Request Accepted"
    msg['From'] = "a@admin.com"
    msg['To'] = user_email

    # Attach HTML part
    part = MIMEText(html_body, 'html')
    msg.attach(part)

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP("localhost", 1025) as server:
            server.sendmail("a@admin.com", user_email, msg.as_string())
        print(f"Email sent to {user_email}")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Task to send email to admin a monthly report about the books issued to user and ratings received by user
@shared_task
def monthly_report():
    smtp_obj = smtplib.SMTP('localhost', 1025)

    # Load and read the template file
    with open("./templates/monthly_report.html") as file:
        template_content = file.read()

    # Create a Jinja2 Template object
    template = Template(template_content)

    # Prepare the feedback data
    feedbacks_data = []
    for feedback in Feedback.query.all():
        user = User.query.get(feedback.user_id)
        # add return date of the book from the BookRequest table where status is accepted and book_id is equal to the feedback.book_id
        book_request = BookRequest.query.filter_by(book_id=feedback.book_id, status='accepted').first()
        if book_request:
            feedback.return_date = book_request.return_date.strftime('%Y-%m-%d')
        feedbacks_data.append({
            'user_name': feedback.user_name,
            'book_name': feedback.book_name,
            'rating': feedback.rating,
            'return_date': feedback.return_date
        })

    # Render the template with the feedback data
    rendered_content = template.render(feedbacks=feedbacks_data)

    # Create and configure the email message
    msg = MIMEMultipart()
    msg['Subject'] = "Monthly Report"
    msg['From'] = "a@admin.com"
    msg['To'] = "a@admin.com"

    # Attach the rendered HTML content
    html = MIMEText(rendered_content, 'html')
    msg.attach(html)

    # Send the email
    smtp_obj.sendmail("a@admin.com", "a@admin.com", msg.as_string())
    smtp_obj.quit()

# If the book is return date approaching then send the alert in morning on return_date asking the user to return the book
@shared_task
def book_return_alert():
    smtp_obj = smtplib.SMTP('localhost', 1025)

    with open("./templates/book_return_alert.html") as file:
        template_content = file.read()

    template = Template(template_content)

    # Ensure you filter the book requests that are accepted and due for return within 1 day
    for book_request in BookRequest.query.filter(
        BookRequest.status == 'accepted',
        BookRequest.return_date <= datetime.utcnow() + timedelta(days=1)
    ).all():
        msg = MIMEMultipart()
        msg['Subject'] = "Book Return Alert"
        msg['From'] = "a@admin.com"
        msg['To'] = book_request.user.email

        # Render the template with the appropriate data
        html_content = template.render(username=book_request.user_name, book_name=book_request.book_name)
        html = MIMEText(html_content, 'html')
        msg.attach(html)

        smtp_obj.sendmail("a@admin.com", book_request.user.email, msg.as_string())

    smtp_obj.quit()
