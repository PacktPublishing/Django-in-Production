# Chapter 6: Caching, Logging, and Throttling

## Table of contents
* [Technical requirements](#technical-requirements)
* [Caching with Django Cache](#caching-with-django-cache)
  * [Using django-cacheops](#using-django-cacheops)
  * [Best practices for caching in Production](#best-practices-for-caching-in-production)
* [Throttling with Django](#throttling-with-django)
  * [Best practices for throttling in production](#best-practices-for-throttling-in-production)
* [Logging with Django](#logging-with-django)
  * [Setting up logging](#setting-up-logging)
  * [Best practices for Logging in production](#best-practices-for-logging-in-production)


## Technical requirements

> [!NOTE]
> 
> To get a basic understanding of Redis one can follow the official documentation of Redis or take one of the Redis courses available. [Redis University](https://university.redis.com/)
> Python official documentation has a fairly simple guide to learning more about the built-in logging module. [Python documentation](https://docs.python.org/3/library/logging.html )

## Caching with Django Cache

Get the Redis endpoint from the Redis lab console. We need the following information to connect to Redis
* Redis endpoint (public endpoint of the Redis instance. For eg - `redis-11193.c281.us-east-1-2.ec2.cloud.redislabs.com:11193`) 
* Redis Username (`default` is user unless you have created a new user)
* Redis Password (Password for the Redis instance, which you can find in the Redis lab console, For eg - `ko15SyJmLWIffmfrpREQgyjsAcrvPkYG`)

configuration to the `settings.py`
```python
CACHES = { 
    'default': { 
        'BACKEND': 'django.core.cache.backends.redis.RedisCache', 
        # 'LOCATION': 'redis://<user>:<password>@<public endpoint>',
        'LOCATION': 'redis://default:ko15SyJmLWIffmfrpREQgyjsAcrvPkYG@redis-11193.c281.us-east-1-2.ec2.cloud.redislabs.com:11193',
    } 
} 
```

Now to test the if redis is working, we can use the following code in the Django shell
```python
from django.core.cache import cache
cache.set('hello', 'World', 600)
cache.get('hello')
```

> [!NOTE]
> Read more about Django framework Cache support [here](https://docs.djangoproject.com/en/latest/topics/cache/#the-per-view-cache)
> 
> Read more about DRF Cache support [Here](https://www.django-rest-framework.org/api-guide/caching/)

### Using django-cacheops

Setup Redis with `django-cacheops` in Django project. 

First, add `cacheops` to the INSTALLED_APPS list in the `settings.py` file
```python
THIRD_PARTY_APPS = [ 
    ... 
    'cacheops', 
    ... 
] 

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + CUSTOM_APPS
```

Now add the following configuration to the `settings.py` file

```python
CACHEOPS_REDIS = { 
    "host": "<public endpoint>",  # Redis endpoint 
    "port": 15014,  # for redis lab, port is 15014 
    "socket_timeout": 3,  # connection timeout in seconds, optional 
    "password": "<REDIS_PASSWORD>", 
} 
```

Now add the following code in the `blog/views.py` file to cache the `get_all_blogs` function
```python
from cacheops import cached
from rest_framework.decorators import api_view


@cached(timeout=60*10)
def get_all_blogs(author_id):
    print('Fetching blogs from database')
    blogs = Blog.objects.filter(author_id=author_id)
    blogs_data = BlogSerializer(blogs, many=True).data
    return blogs_data


@api_view(['GET'])
def get_blogs_by_author(request):
    author_id = request.GET.get('author_id')
    blogs = get_all_blogs(author_id)
    return Response({'blogs': blogs})
```

This will cache the `get_all_blogs` function for 10 minutes. We can verify this by checking the output in the terminal. If the function is cached, then the logs will not print `Fetching blogs from database` message.

Cacheops also provides interface to invalidate the cache. We can invalidate the cache by using the following code
```python
from blog.views import get_all_blogs

get_all_blogs.invalidate(12) # 12 is the author_id for which we want to invalidate the cache

# We can also invalidate the cache for all the author_id
get_all_blogs.invalidate()
```

---
Cacheops also provides an option to cache all the queries for a particular model. We can do this by adding the following code in the `settings.py` file
```python
CACHEOPS = { 
    # Cache any User.objects.get() calls for 15 minutes 
    # This also includes .first() and .last() calls, 
    # as well as request.user or post.author access, 
    # where Blog.author is a foreign key to auth.User 
    'auth.user': {'ops': 'get', 'timeout': 60*15}, 
 
    # Cache all gets and queryset fetches 
    # to other django.contrib.auth models for an hour 
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60} 
} 
```

---
Cacheops also provides a way to auto invalidation of cached results on any data source update. We can do this by adding the following code in the `blog/views.py` file
```python
from cacheops import cached_as
from blog.models import Blog

@cached_as(Blog, timeout=60*10)
def get_all_blogs(author_id):
    print('Fetching blogs from database')
    blogs = Blog.objects.filter(author_id=author_id)
    blogs_data = BlogSerializer(blogs, many=True).data
    return blogs_data
```


### Best practices for caching in Production

No code applicable to this section

## Throttling with Django

To enable throttling in Django, we need to add the following configuration to the `settings.py` file
```python
REST_FRAMEWORK = { 
    'DEFAULT_THROTTLE_RATES': { 
        'anon': '100/day', 
        'user': '1000/day', 
    }
} 
```
Now we can add the following code to the `blog/views.py` file to throttle the APIs for anonymous users

```python
from rest_framework.views import APIView 
from rest_framework.throttling import AnonRateThrottle 
from rest_framework.response import Response
 
class BlogApiView(APIView): 
    throttle_classes = [AnonRateThrottle] 
    def get(self, request):
        content = {'status': 'request was permitted'}
        return Response(content)    
```
---

Django provides scope-based throttling. We can do this by adding the following code to the `settings.py` file
```python
REST_FRAMEWORK = { 
    'DEFAULT_THROTTLE_RATES': { 
        'blog_limit': '1000/day', 
        'blog_2_limit': '1000/day', 
    } 
} 
```

We can also throttle the APIs based on the user and scope. We can do this by adding the following code to the `blog/views.py` file

```python
from rest_framework.views import APIView
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.response import Response
 
class BlogApiView(APIView): 
    throttle_classes = [ScopedRateThrottle] 
    throttle_scope = 'blog_limit' 
    def get(self, request):
        content = {'status': 'request was permitted'}
        return Response(content)  

class BlogDetailApiView(APIView): 
    throttle_classes = [ScopedRateThrottle] 
    throttle_scope = 'blog_limit' 
    def get(self, request):
        content = {'status': 'request was permitted'}
        return Response(content)

class Blog2ApiView(APIView): 
    throttle_classes = [ScopedRateThrottle] 
    throttle_scope = 'blog_2_limit'
    def get(self, request):
        content = {'status': 'request was permitted'}
        return Response(content)
```


### Best practices for throttling in production

No code applicable to this section

## Logging with Django

> [!NOTE]
> If you want to deep-dive into detailed configurations, please go through the python logging module official documentation and Django logging documentation. [Read more](https://docs.djangoproject.com/en/stable/topics/logging/)

### Setting up logging

To setup logging in Django, we need to add the following configuration to the `settings.py` file
```python
LOGGING = { 
    "version": 1, 
    "disable_existing_loggers": False, 
    "formatters": {"verbose": {"format": "%(asctime)s %(process)d %(thread)d %(message)s"}}, 
    "loggers": { 
        "django_default": { 
            "handlers": ["django_file"], 
            "level": "INFO", 
        }, 
    }, 
    "handlers": { 
        "django_file": { 
            "class": "common.custom_log_handlers.MakeRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django_logs.log"), 
            "maxBytes": 1024 * 1024 * 10,  # 10MB 
            "backupCount": 10, 
            "formatter": "verbose" 
        }, 
    }, 
} 
```
> [!NOTE]
> We are not using the default logging configuration. We are using our own custom log handler class configuration. 
> The default logging configuration provided by Python `logging.handlers.RotatingFileHandler` would not create the `log` folder automatically.
> Log files would be created in the `log` folder, so we need to create the `log` folder manually. 

We want to automatically create the `log` folder, we can add the following code to `common/custom_log_handler.py` file
```python
import os
from logging.handlers import RotatingFileHandler


class MakeRotatingFileHandler(RotatingFileHandler):
    def __init__(self, filename, mode="a", maxBytes=1024 * 1024 * 10, backupCount=0, encoding=None, delay=0):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        RotatingFileHandler.__init__(self, filename, mode, maxBytes, backupCount, encoding, delay)
```


Let us create a utility function to log the events. We can add the following code to the `common/logging_util.py` file
```python
import json
import logging

from common.localthread_middleware import get_current_user_id
from common.localthread_middleware import get_txid

def log_event(event_name, log_data, logging_module="django_default", level="INFO"):
    """
    :param event_name: Event name which you are logging
    :param log_data: The data you want to log, this can be anything serializable
    :param logging_module: If you want to use any custom module for logging, define it in Django settings
    :param level: Level for which you are logging.
    """
    logger = logging.getLogger(logging_module)

    try:
        msg = {"ev": event_name, "data": log_data, "txid": get_txid()}
        user_id = get_current_user_id()
        if user_id:
            msg["uid"] = user_id
        logger.log(msg=json.dumps(msg), level=getattr(logging, level))
    except Exception as e:
        print('Error')  # user error monitoring tool
        return
```

Now we need to add the following code to the `common/localthread_middleware.py` file
```python
from threading import local
from uuid import uuid4
_thread_locals = local()


def get_current_request():
    """Returns the request object in thread local storage."""
    return getattr(_thread_locals, "request", None)


def get_current_user():
    """Returns the current user, if exist, otherwise returns None."""
    request = get_current_request()
    if request:
        return getattr(request, "user", None)

def get_txid():
    """Returns the current transaction id, if exist, otherwise returns None."""
    return getattr(_thread_locals, "txid", None)

def get_current_user_id():
    """Returns authenticated user's id for this thread, if not present returns 0."""
    user = get_current_user()
    if user and user.id:
        return user.id
    return 0


class PopulateLocalsThreadMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print("custom middleware before next middleware/view")
        # Populate the request object in thread local storage to be accessible anywhere
        _thread_locals.request = request
        _thread_locals.txid = str(uuid4())
        # the view (and later middleware) are called.
        response = self.get_response(request)
        # Clean up the thread local storage
        _thread_locals.request = None
        _thread_locals.tx_id = None
        print("custom middleware after response is returned")
        return response
```

Now we need to add the following code to the `settings.py` file
```python
MIDDLEWARE = [ 
    ... 
    'common.localthread_middleware.PopulateLocalsThreadMiddleware', 
    ... 
] 
```

Now we can use the `log_event` function to log the events. 
For example, we can add the following code to the `blog/views.py` file.

```python
from common.logging_util import log_event

def get_blogs_by_author(request):
    author_id = request.GET.get('author_id')
    log_event('get_blogs_by_author', {'author_id': author_id})
    blogs = get_all_blogs(author_id)
    return Response({'blogs': blogs})
```

Now we can see the logs in the `log/django_logs.log` file.

### Best practices for Logging in production

No code applicable to this section
