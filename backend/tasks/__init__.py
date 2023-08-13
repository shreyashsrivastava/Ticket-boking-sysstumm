from celery import Celery

celery_app = Celery('booking_tasks', broker_url='redis://127.0.0.1:6379/0', backend='redis://127.0.0.1:6379', include=['tasks.tasks'])