import os

from celery import Celery

os.environ.setdefault("CONNECTION_MAX_AGE", "0")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
celery_app = Celery("CastForm")
celery_app.config_from_object("django.conf:settings", namespace="CELERY")
celery_app.autodiscover_tasks()
