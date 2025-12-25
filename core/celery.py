import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE",'core.settings') # celery run outside djnago so ithi tell here is seeting of celery
app = Celery('core') 
app.config_from_object('django.conf:settings',namespace="CELERY")
app.autodiscover_tasks() # this  will automatically find @shared_task or task.py function  
