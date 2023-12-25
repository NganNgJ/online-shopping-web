from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sellweb.settings')

app = Celery('sellweb')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.broker_url = 'pyamqp://user:password@rabbitmq:5672//'

app.autodiscover_tasks()