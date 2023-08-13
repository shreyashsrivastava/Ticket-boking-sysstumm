from celery import Celery
from celery.schedules import crontab

celery_app = Celery('booking_tasks', broker_url='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379', include=['tasks.tasks'])

# app.py
celery_app.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'accounts.tasks.send_daily_reminders',
        'schedule': crontab(hour=19, minute=0),  # 7:00 PM daily
    },
}
