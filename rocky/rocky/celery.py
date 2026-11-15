import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yourproject.settings')

app = Celery('yourproject')

# Load settings from Django settings, using CELERY_ namespace
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all apps
app.autodiscover_tasks()
