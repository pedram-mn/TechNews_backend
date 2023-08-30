from __future__ import absolute_import, unicode_literals
import os

from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TechNews_back.settings')

app = Celery('TechNews_back')
app.conf.enable_utc = False

app.conf.update(timezone='Asia/Tehran')

app.config_from_object(settings, namespace='CELERY')

# Celery Beat Settings
app.conf.beat_schedule = {
    'extract_zoomit_news_every_day': {
        'task': 'news.tasks.extract_zoomit_news',
        'schedule': 300.0,
    }
}

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
