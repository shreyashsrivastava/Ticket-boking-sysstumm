from datetime import datetime, time
from flask_mail import Message
from website import mail
# from tasks import celery_app
from . import celery_app

@celery_app.task(name="send_daily_reminders")
def send_daily_reminders():
    # Get the current date and time
    current_time = datetime.now().time()

    # Set the time for the evening reminder (e.g., 7:00 PM)
    evening_time = time(19, 0)

    # Check if it's the evening
    if current_time >= evening_time:
        users_to_remind = get_users_to_remind()

        # Send reminders to the users
        for user in users_to_remind:
            send_reminder_email(user.email)

def get_users_to_remind():
    from accounts.models import User
    from ticket.models import Ticket
    
    users = User.query.all()
    tickets = Ticket.query.all()
    for user in users:
        for ticket in tickets:
            if ticket.user_id == user.id:
                users.remove(user)
    return users

def send_reminder_email(email):
    subject = "Daily Reminder"
    body = "Hello! It looks like you haven't visited or booked anything yet. Please consider visiting or booking something today."

    message = Message(subject=subject, recipients=[email], body=body)
    mail.send(message)


from celery import Celery
import sqlite3
import csv

@celery_app.task
def generate_csv_task():
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()

    cursor.execute('SELECT show.* FROM show,venue where show.venue_id = venue.id')
    data = cursor.fetchall()

    conn.close()

    csv_data = []
    csv_data.append([description[0] for description in cursor.description])
    csv_data.extend(data)

    csv_content = '\n'.join([','.join(map(str, row)) for row in csv_data])
    return csv_content