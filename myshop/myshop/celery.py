import os
from celery import Celery

#set the default Django settings module for the 'Celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')

app.config_from_object('django.conf:setting', namespace='CELERY')
app.autodiscover_tasks()