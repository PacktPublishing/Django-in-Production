# Chapter 8: Using Celery with Django

## Table of contents
* [Technical requirements](#technical-requirements)
* [Asynchronous programming in Django](#asynchronous-programming-in-django)
* [Using Celery with Django](#using-celery-with-django)
  * [Integrating Celery and Django](#integrating-celery-and-django)
  * [Interfaces of Celery](#interfaces-of-celery)
  * [Best practices using for Celery](#best-practices-using-for-celery)
* [Using Celery Beat with Django](#using-celery-beat-with-django)


## Technical requirements

No code applicable to this section

> [!NOTE]
> 
> Join the Discord server "[Django in Production](https://discord.gg/FCrGUfmDyP)" for direct support from the author as you follow the instructions in the book. Feel free to reach out for any help or clarifications needed. https://discord.gg/FCrGUfmDyP.


## Asynchronous programming in Django
Django, official documentation [Read more](https://docs.djangoproject.com/en/4.1/topics/async/#performance )

## Using Celery with Django

### Integrating Celery and Django

Install Celery
```bash
pip install celery
```

Create a `config/celery.py` file 
```python
import os 
from celery import Celery 
 
celery_settings_value = "config.settings"  
# change config with folder name where your settings.py file is present. 
 
os.environ.setdefault("DJANGO_SETTINGS_MODULE", celery_settings_value) 
 
app = Celery("config")  
# change config with folder name where your settings.py file is present. 
 
app.config_from_object("django.conf:settings", namespace="CELERY") 
app.autodiscover_tasks() 
task = app.task 
 
@app.task(bind=True) 
def debug_task(self, data): 
    print(data) 
```

Added celery to settings in `config/settings.py` file. We are using redis as a broker and result backend for celery, the credentials are for redislabs.com.
```python
REDIS_CONNECTION_STRING = 'redis://default:ko15SyJmLWIffmfrpREQgyjsAcrvPkYG@redis-11193.c281.us-east-1-2.ec2.cloud.redislabs.com:11193'

CELERY_BROKER_URL = REDIS_CONNECTION_STRING
CELERY_RESULT_BACKEND = REDIS_CONNECTION_STRING
```
Run celery worker to start the celery server
```bash
celery --app=config worker --loglevel=INFO
```

Now let us use celery task in our Django project. Update a `blog/view.py` file
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from config.celery import debug_task
@api_view(['GET'])
def verify_blog(request):
    verify_word = request.GET.get('verify_word')
    debug_task.delay(f"Celery Task verification: {verify_word}")
    return Response({'status': 'success'})
```

Add the view to the `blog/urls.py` file
```python
from django.urls import path
from blog import views

urlpatterns = [
    path('verify/', views.verify_blog),
]
```

Run the Django server
```bash
python manage.py runserver
```

Open the browser and hit the url `http://127.0.0.1:8000/blog/verify/?verify_word=abc` to see the output in the celery worker terminal.
```bash
[2023-12-03 15:37:31,441: INFO/MainProcess] mingle: searching for neighbors
[2023-12-03 15:37:35,428: INFO/MainProcess] mingle: all alone
[2023-12-03 15:37:40,348: INFO/MainProcess] celery@Arghyas-MacBook-Pro-2.local ready.
[2023-12-03 15:40:39,488: INFO/MainProcess] Task config.celery.debug_task[4e67553e-48d2-41fc-af60-34fb0a8e6cac] received
[2023-12-03 15:40:39,490: WARNING/ForkPoolWorker-8] Celery Task verification: abc
[2023-12-03 15:40:40,544: INFO/ForkPoolWorker-8] Task config.celery.debug_task[4e67553e-48d2-41fc-af60-34fb0a8e6cac] succeeded in 1.0551899160200264s: None
[2023-12-03 15:40:43,424: INFO/MainProcess] Task config.celery.debug_task[08976c33-8b35-40c6-b307-f494d8fdb8d8] received
[2023-12-03 15:40:43,431: WARNING/ForkPoolWorker-8] Celery Task verification: abc
[2023-12-03 15:40:43,923: INFO/ForkPoolWorker-8] Task config.celery.debug_task[08976c33-8b35-40c6-b307-f494d8fdb8d8] succeeded in 0.49289650001446716s: None
```


> [!NOTE]
> Celery doesn't support native hot reloading. But we can use `watchdog` package for it, [read more](https://github.com/gorakhargosh/watchdog)

### Interfaces of Celery

Create a `blog/tasks.py` file
```python
from config.celery import task 

@task(bind=True) 
def send_email_to_followers(self, author_id, blog_id): 
    print(f"Sending email to followers of author {author_id} for blog {blog_id}") 
```

Update the `blog/view.py` file
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.tasks import send_email_to_followers

@api_view(['GET'])
def publish_blog(request):
    blog_id = request.GET.get('blog_id')
    author_id = request.GET.get('author_id')
    print(f"Publishing blog {blog_id}")
    send_email_to_followers.delay(author_id, blog_id)
    return Response({'status': 'success'})
```

Add the view to the `blog/urls.py` file
```python
urlpatterns = [
    path('publish/', views.publish_blog),
]
```


### Best practices using for Celery

No code applicable to this section

## Using Celery Beat with Django

Create a periodic task that runs every 1 minute interval-  
```python
from config.celery import app 
from config.celery import task
from celery.schedules import crontab
 
@app.on_after_finalize.connect 
def setup_basic_periodic_tasks(sender, **kwargs): 
    sender.add_periodic_task( 
       crontab(), 
       test_task.s("periodic task") 
    ) 
 
@task(bind=True) 
def test_task(self, value): 
    print(value)
```

Run celery beat to start the celery beat server
```bash
celery --app=config beat --loglevel=INFO
```

Open a new terminal to start the celery worker
```bash
celery --app=config worker --loglevel=INFO
```

Now every minute we will see the output in the celery worker terminal
```bash
[2023-12-03 15:37:31,441: INFO/MainProcess] mingle: searching for neighbors
[2023-12-03 15:37:35,428: INFO/MainProcess] mingle: all alone
[2023-12-03 17:49:00,748: WARNING/ForkPoolWorker-8] periodic task
[2023-12-03 17:49:01,251: INFO/ForkPoolWorker-8] Task author.tasks.demo_task[afe12727-d72a-40d9-aaad-cb94280d5b4f] succeeded in 0.5037782920117024s: None
[2023-12-03 17:50:01,026: INFO/MainProcess] Task author.tasks.demo_task[e0df97ec-008d-42ea-8ed6-d8b4c738e676] received
[2023-12-03 17:50:01,028: WARNING/ForkPoolWorker-8] periodic task
[2023-12-03 17:50:01,537: INFO/ForkPoolWorker-8] Task author.tasks.demo_task[e0df97ec-008d-42ea-8ed6-d8b4c738e676] succeeded in 0.5090533340116963s: None
[2023-12-03 17:51:01,007: INFO/MainProcess] Task author.tasks.demo_task[26003d35-175a-4ea5-b8fd-2f4447544df5] received
[2023-12-03 17:51:01,258: WARNING/ForkPoolWorker-8] periodic task
[2023-12-03 17:51:01,764: INFO/ForkPoolWorker-8] Task author.tasks.demo_task[26003d35-175a-4ea5-b8fd-2f4447544df5] succeeded in 0.5066564579901751s: None
```

And in the celery beat terminal we would see the following output
```bash
LocalTime -> 2023-12-03 17:30:16
Configuration ->
    . broker -> redis://default:**@redis-11193.c281.us-east-1-2.ec2.cloud.redislabs.com:11193//
    . loader -> celery.loaders.app.AppLoader
    . scheduler -> celery.beat.PersistentScheduler
    . db -> celerybeat-schedule
    . logfile -> [stderr]@%INFO
    . maxinterval -> 5.00 minutes (300s)
[2023-12-03 17:30:16,602: INFO/MainProcess] beat: Starting...
[2023-12-03 17:30:17,368: INFO/MainProcess] Scheduler: Sending due task author.tasks.demo_task('periodic task') (author.tasks.demo_task)
[2023-12-03 17:31:00,010: INFO/MainProcess] Scheduler: Sending due task author.tasks.demo_task('periodic task') (author.tasks.demo_task)
[2023-12-03 17:32:00,000: INFO/MainProcess] Scheduler: Sending due task author.tasks.demo_task('periodic task') (author.tasks.demo_task)
[2023-12-03 17:33:00,000: INFO/MainProcess] Scheduler: Sending due task author.tasks.demo_task('periodic task') (author.tasks.demo_task)
[2023-12-03 17:34:00,000: INFO/MainProcess] Scheduler: Sending due task author.tasks.demo_task('periodic task') (author.tasks.demo_task)
```

