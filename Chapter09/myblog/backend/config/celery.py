import os
from celery import Celery

celery_settings_value = "config.settings"
# change <project name> with folder name where your settings.py file is present.

os.environ.setdefault("DJANGO_SETTINGS_MODULE", celery_settings_value)

app = Celery("config")
# change <project name> with folder name where your settings.py file is present.

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

task = app.task



@app.task(bind=True)
def debug_task(self, data):
    print(data)
