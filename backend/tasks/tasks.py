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

        subject = "Daily Reminder"
        body = "Hello! It looks like you haven't visited or booked anything yet. Please consider visiting or booking something today."
    
        # Send reminders to the users
        for user in users_to_remind:
            send_email(user.email, subject, body)

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

def send_email(email, subject, body, attachment_file_path=None):
    message = Message(subject=subject, recipients=[email], body=body)
    if attachment_file_path:
        # Attach the CSV file to the email
        with open(attachment_file_path, 'rb') as csv_file:
            message.attach(
                filename=f'theater_data.csv',
                content_type='text/csv',
                data=csv_file.read()
            )
    mail.send(message)


@celery_app.task
def generate_csv_task(venue_id):
    csv_content = generate_csv(venue_id)
    with open('theater_data.csv', 'w') as csv_file:
        csv_file.write(csv_content)
    admin_users = get_admin_users()
    for user in admin_users:
        send_email(user.email, "Theater Data", "Here is the data for the theater.", attachment_file_path="theater_data.csv")
        
def get_admin_users():
    from accounts.models import User
    
    return User.query.filter_by(is_admin=True).all()
    
def generate_csv(venue_id):
    import sqlite3
        
    conn = sqlite3.connect('project.db')
    cursor = conn.cursor()

    cursor.execute(f'SELECT show.* FROM show where show.venue_id = {venue_id}')
    data = cursor.fetchall()

    conn.close()

    csv_data = []
    csv_data.append([description[0] for description in cursor.description])
    csv_data.extend(data)

    csv_content = '\n'.join([','.join(map(str, row)) for row in csv_data])
    return csv_content