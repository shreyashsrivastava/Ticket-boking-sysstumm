import logging
from datetime import datetime, time
from flask_mail import Message
from website import mail
from . import celery_app
from celery.schedules import crontab

# Set up logging
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(filename='email_log.txt', level=logging.INFO, format=log_format)



@celery_app.task(name="send_daily_reminders")
def send_daily_reminders():
    from website import app
    with app.app_context():
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
            print("Users to remind: ", users_to_remind)
            for user in users_to_remind:
                send_email(user.email, subject, body)

def get_users_to_remind():
    from accounts.models import User
    from ticket.models import Ticket
    
    users = User.query.all()
    tickets = Ticket.query.all()
    for user in users:
        for ticket in tickets:
            if ticket.user == user.id:
                try:
                    users.remove(user)
                except ValueError:
                    continue
    return users

def send_email(email, subject, body, attachment_file_path=None):
    try:
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
        logging.info(f"Email sent successfully to {email}")
    except Exception as e:
        logging.error(f"Error sending email: {e}", exc_info=True)

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_tas(crontab(hour=19, minute=0), send_daily_reminders.s(), name='send_daily_reminders')

@celery_app.task
def generate_csv_task(venue_id):
    from website import app
    with app.app_context():
        csv_file_path = generate_csv(venue_id)
        admin_users = get_admin_users()
        for user in admin_users:
            send_email(user.email, "Theater Data", "Here is the data for the theater.", attachment_file_path=csv_file_path)
        delete_csv_file(csv_file_path)
        
def get_admin_users():
    from accounts.models import User
    
    return User.query.filter_by(is_admin=True).all()
    
def generate_csv(venue_id):
    import csv
    from shows.models import Show
    from ticket.models import Ticket
    
    data = Show.query.filter_by(venue_id=venue_id).all()
    csv_file_path = 'shows_data.csv'

    csv_header = ['ID', 'Name', 'Rating', 'Tag', 'Ticket Price', 'Updated Price', 'Date', 'Number of tickets sold']
    
    # Prepare the CSV data rows
    csv_data = []
    for show in data:
        tickets_count = len(Ticket.query.filter_by(show=show.id).all())
        csv_data.append([
            show.id,
            show.name,
            show.rating,
            show.tag,
            show.ticket_price,
            show.updated_price,
            show.date.strftime('%Y-%m-%d'),  # Format the date as 'YYYY-MM-DD'
            tickets_count
        ])
        
    # Write the data to the CSV file
    with open(csv_file_path, mode='w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(csv_header)
        writer.writerows(csv_data)
    
    return csv_file_path

def delete_csv_file(csv_file_path):
    import os
    try:
        # Delete the CSV file
        os.remove(csv_file_path)
        print(f"CSV file '{csv_file_path}' has been deleted.")
    except OSError as e:
        print(f"Error deleting CSV file: {e}")