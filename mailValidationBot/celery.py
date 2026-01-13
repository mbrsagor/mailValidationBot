from celery import Celery
import os

# Celery Configuration
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mailValidationBot.settings')
app = Celery('mailValidationBot')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
