from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from account.views import calculate_bonus


# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aroma.settings')
app = Celery('aroma')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


@app.task(bind=True)
def bonus_calculation(self):
    print('Request: {0!r}'.format(self.request))
    calculate_bonus()



