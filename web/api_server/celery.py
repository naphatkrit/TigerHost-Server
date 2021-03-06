"""The Celery module, use absolute import so that this doesn't
conflict with the actual Celery library. This module sets up
a Celery app object that tasks can register to.
"""
from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings  # noqa

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.dev')

app = Celery('api_server')


# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
