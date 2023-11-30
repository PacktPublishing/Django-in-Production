# Using Celery with Django

## Table of contents
* [Technical requirements](#technical-requirements)
* [Asynchronous programming in Django](#asynchronous-programming-in-django)
* [Using Celery with Django](#using-celery-with-django)
  * [Integrating Celery and Django](#integrating-celery-and-django)
  * [Interfaces of Celery](#interfaces-of-celery)
  * [Best practices using for Celery](#best-practices-using-for-celery)
* [Using Celery Beat with Django](#using-celery-beat-with-django)


## Technical requirements


## Asynchronous programming in Django
Django, official documentation [Read more](https://docs.djangoproject.com/en/4.1/topics/async/#performance )

## Using Celery with Django

### Integrating Celery and Django

new celery.py file in the same folder where we have settings.py
```python
import os 
from celery import Celery 
 
celery_settings_value = "<project name>.settings"  
# change <project name> with folder name where your settings.py file is present. 
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", celery_settings_value) 
 
app = Celery("<project name>")  
# change <project name> with folder name where your settings.py file is present. 
 
app.config_from_object("django.conf:settings", namespace="CELERY") 
app.autodiscover_tasks() 
task = app.task 
 
@app.task(bind=True) 
def debug_task(self, data): 
    print(data) 
```

Read more about watchdog at [watchdog](https://github.com/gorakhargosh/watchdog)

### Interfaces of Celery

create a blog/tasks.py file
```python
from blog import private 
from config.celery import app 
from config.celery import task 
 
@task(bind=True) 
def send_email_to_followers(self, author_id, blog_id): 
    follower_list = private.get_follower_list(author_id) 
    for follower_id in follower_list: 
        private.send_follower_email(follower_id, blog_id) 
```


### Best practices using for Celery


## Using Celery Beat with Django

every 2 hours, 5 min and trigger test_task:  
```python
from config.celery import app 
from config.celery import task 
 
@app.on_after_finalize.connect 
def setup_basic_periodic_tasks(sender, **kwargs): 
    sender.add_periodic_task( 
       crontab(minute=5, hour="*/2"), 
       test_task.s("periodic task") 
    ) 
 
@task(bind=True) 
def test_task(self, value): 
    print(value) 
```
