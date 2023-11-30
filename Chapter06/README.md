# Caching, Logging, and Throttling

## Table of contents
* [Technical requirements](#technical-requirements)
* [Caching with Django Cache](#caching-with-django-cache)
  * [Using django-cacheops](#using-django-cacheops)
  * [Best practices for caching in Production](#best-practices-for-caching-in-production)
* [Throttling with Django](#throttling-with-django)
  * [Best practices for throttling in production](#best-practices-for-throttling-in-production)
* [Logging with Django](#logging-with-django)
  * [Setting up logging](#setting-up-logging)
  * [Best practices for throttling in production](#best-practices-for-throttling-in-production)


## Technical requirements

To get a basic understanding of Redis one can follow the official documentation of Redis or take one of the Redis courses available. [Redis University](https://university.redis.com/)
Python official documentation has a fairly simple guide to learning more about the built-in logging module. [Python documentation](https://docs.python.org/3/library/logging.html )

## Caching with Django Cache

configuration to the settings.py
```python
CACHES = { 
    'default': { 
        'BACKEND': 'django.core.cache.backends.redis.RedisCache', 
        'LOCATION': 'redis://<user>:<password>@<public endpoint>', 
    } 
} 
```
Django [CACHES](https://docs.djangoproject.com/en/latest/topics/cache/#the-per-view-cache)
DRF [Read more](https://www.django-rest-framework.org/api-guide/caching/)

### Using django-cacheops

configure Redis with django-cacheops. First, add cacheops to the INSTALLED_APPS list in the settings.py file
```python
CACHEOPS_REDIS = { 
    "host": "<public endpoint>",  # Redis endpoint 
    "port": 15014,  # for redis lab, port is 15014 
    "socket_timeout": 3,  # connection timeout in seconds, optional 
    "password": "<REDIS_PASSWORD>", 
} 
```

Blogs written by a given author
```python
@cached(timeout=60*10) 
def get_all_blogs(author_id): 
    blogs = models.Blog.objects.filter(author_id=author_id) 
    return list(blogs) 
```

Configure cacheops in django settings.py file
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

### Best practices for caching in Production

## Throttling with Django

```python
from rest_framework.views import APIView 
from rest_framework.throttling import AnonRateThrottle 
 
class BlogApiView(APIView): 
    throttle_classes = [AnonRateThrottle] 
    ...  
```
total rate limit is going to be distributed among both the APIs while AuthorApiView shall have an independent limit
```python
from rest_framework.views import APIView 
from rest_framework.throttling import AnonRateThrottle 
 
class BlogApiView(APIView): 
    throttle_classes = [ScopeRateThrottle] 
    throttle_scope = 'blog_limit' 
    ...  

class BlogDetailApiView(APIView): 
    throttle_classes = [ScopeRateThrottle] 
    throttle_scope = 'blog_limit' 
    ...  

class AuthorApiView(APIView): 
    throttle_classes = [ScopeRateThrottle] 
    throttle_scope = 'author_limit' 
    ...  
```

### Best practices for throttling in production

## Logging with Django

If you want to deep-dive into detailed configurations, please go through the python logging module official documentation and Django logging documentation. [Read more](https://docs.djangoproject.com/en/stable/topics/logging/)

### Setting up logging

Configure logging in settings.py
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
            "class": " logging.handlers.RotatingFileHandler", 
            "filename": "path/to/django_logs.log", 
            "maxBytes": 1024 * 1024 * 10,  # 10MB 
            "backupCount": 10, 
            "formatter": "verbose" 
        }, 
    }, 
} 
```

Logging events
```python
import json 
import logging 
from threading import local 
 
def log_event(event_name, log_data, logging_module="django_default", level="INFO"): 
    """ 
    :param event_name: Event name which you are logging  
    :param log_data: The data you want to log, this can be anything serializable 
    :param logging_module: If you want to use any custom module for logging, define it in Django settings 
    :param level: Level for which you are logging. 
    """ 
    logger = logging.getLogger(logging_module) 
 
    try: 
        msg = {"ev": event_name, "data": log_data} 
        user_id = get_current_user_id() 
        if user_id: 
            msg["uid"] = user_id 
        logger.log(msg=json.dumps(msg), level=getattr(logging, level)) 
    except Exception as e: 
        print('Error') # user error monitoring tool 
        return 
 
_thread_locals = local() 
 
def get_current_user_id(): 
    """Returns user's id, if not present returns 0.""" 
    current_req = getattr(_thread_locals, "request", None) 
    current_user = getattr(current_req, "user", None) 
    if current_user and current_user.id: 
        return current_user.id 
    return 0 
```

### Best practices for throttling in production

