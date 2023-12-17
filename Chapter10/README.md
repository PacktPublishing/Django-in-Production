# Chapter 10: Exploring Conventions in Django

## Table of contents
* [Technical requirements](#technical-requirements)
* [Code structuring for Django Projects](#code-structuring-for-django-projects)
    * [Creating files as per functionalities](#creating-files-as-per-functionalities)
    * [Avoiding Circular Dependency](#avoiding-circular-dependency)
    * [Creating a “Common” App](#creating-a-common-app)
    * [Working with Exceptions and Errors](#working-with-exceptions-and-errors)
    * [Using Feature flags](#using-feature-flags)
* [Configuring Django for production](#configuring-django-for-production)
    * [Setting up CORS](#setting-up-cors)
    * [Exploring WSGI](#exploring-wsgi)


## Technical requirements

No code applicable to this section

## Code structuring for Django Projects

No code applicable to this section

### Creating files as per functionalities

No code applicable to this section

### Avoiding Circular Dependency


Circular import error example 
```python
ImportError: cannot import name '<name>' from partially initialized module '<module>' (most likely due to a circular import).
```

### Creating a “Common” App

No code applicable to this section

### Working with settings file for production

Use os module to get the environment variables and load them in the settings.py file

```python
DATABASES = { 
    "default": { 
        "ENGINE": os.environ.get("SQL_ENGINE"), 
        "NAME": os.environ.get("SQL_DATABASE"), 
        "USER": os.environ.get("SQL_USER", "user"), 
        "PASSWORD": os.environ.get("SQL_PASSWORD", "password"), 
        "HOST": os.environ.get("SQL_HOST", "localhost"), 
        "PORT": os.environ.get("SQL_PORT", "5432"), 
    } 
} 
```

The environment values can be loaded from a `.env` file. For example, the .env file can be created in the root directory of the project and the following values can be added to it:
```
SQL_ENGINE=django.db.backends.postgresql
SQL_DATABASE=django_db
SQL_USER=django_user
SQL_PASSWORD=django_password
SQL_HOST=localhost
SQL_PORT=5432
```

### Working with Exceptions and Errors

Sending custom error messages to client when an exception occurs helps in debugging the application better. 
For example a user is trying to get a blog that is not present in the database. In this case, we can send a custom error message to the user saying that the blog is not found. 
Our view function `blog/views.py` can be modified 

```python
@api_view(['GET'])
def get_blog_by_id(blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
    except Blog.DoesNotExist:
        return Response(
          status=status.HTTP_404_NOT_FOUND,
          data={'error': 'Blog does not exist',
                'error_code': 'BLG0012'}
        )
    blog_data = BlogSerializer(blog).data
    return Response({'blog': blog_data}, status=status.HTTP_200_OK)
```


Integrate Error monitoring tools like [Rollbar] (https://rollbar.com/), [Sentry] (https://sentry.com)

### Using Feature flags

To create a custom feature flag, we can create a model in the database and store the value of the flag in the database.

Add a new model in `common/models.py` file
```python
class KeyValueStore(models.Model): 
    key = models.CharField(max_length=255, unique=True) 
    value = models.JSONField() 
 
    def __str__(self): 
        return self.key 
```

Add the model to the admin site in `common/admin.py` file
```python
from django.contrib import admin
from common.models import KeyValueStore

admin.site.register(KeyValueStore)
```

Add a new migration and migrate the database
```bash
python manage.py makemigrations
python manage.py migrate
```

Now to use the feature flag, we can create a function in `common/public.py` file

```python
from common import models

def get_current_config(key_name):
  try:
    return models.KeyValueStore.objects.get(key=key_name).value
  except models.KeyValueStore.DoesNotExist:
    return {}
```

```python
from common import public

def get_current_gateway(): 
   return public.get_current_config('payment_gateway')
 
def get_payment_gateway(): 
    payment_config = get_current_gateway() 
    if payment_config.get('name') == 'stripe': 
        return 'stripe' 
    elif payment_config.get('name') == 'paypal': 
        return 'PayPal' 
    return 'stripe' 
 
def make_payment(request): 
    # do something related to payment 
    payment_gateway = get_payment_gateway() 
    # process payment 
```

## Configuring Django for production

### Setting up CORS

Install django-cors-headers
```bash
pip install django-cors-headers
```

Now add the following in the settings.py file
```python
INSTALLED_APPS = [ 
    ..., 
    "corsheaders", 
    ..., 
] 

MIDDLEWARE = [ 
    ..., 
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    ..., 
] 

CORS_ALLOWED_ORIGINS = [ 
    "https://example.com", 
    "https://sub.example.com", 
    "http://127.0.0.1:8000",
    "0.0.0.0",
    "127.0.0.1"
]
```

`CORS_ALLOWED_ORIGINS` config is used to specify the list of domains that are allowed to access the APIs.

### Exploring WSGI

WSGI is a specification that describes how a web server communicates with web applications.

WSGI is a Python standard described in PEP 3333. It is a simple calling convention for web servers to forward requests to web applications or frameworks written in the Python programming language.

Install gunicorn
```bash
pip install gunicorn
```

Also remember to add the following in the settings.py file
```python
ALLOWED_HOSTS = [
    "0.0.0.0"
]
```

To run the application using gunicorn, run the following command
```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers=4 --max-requests=512 --max-requests-jitter=64 
```

Now when we run the application using gunicorn, we can see that the application is running on port 8000 on our browser.

Open the browser and go to http://0.0.0.0:8000/blog/hello-world/?format=json we can see the application running.