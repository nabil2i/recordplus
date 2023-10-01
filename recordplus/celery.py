from __future__ import absolute_import, unicode_literals

import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'recordplus.settings')

celery = Celery('recordplus')

# location of config variables
celery.config_from_object('django.conf:settings', namespace='CELERY')
celery.conf.broker_connection_retry_on_startup = True
celery.autodiscover_tasks()

# CELERY_TASK_QUEUE = 'transcription_queue'

