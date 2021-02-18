import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

app = Celery('blog')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'scraping-task-odd_hour': {
        'task': 'posts.tasks.add_posts_rss',
        'schedule': crontab(hour='1-23/2'),
    },
}
