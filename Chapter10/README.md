# Exploring Conventions in Django

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

## Code structuring for Django Projects

### Creating files as per functionalities

### Avoiding Circular Dependency

### Creating a “Common” App

### Working with Exceptions and Errors

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

Integrate Error monitoring tools like [Rollbar] (https://rollbar.com/), [Sentry] (https://sentry.com)

### Using Feature flags

```python
def get_current_gateway(): 
   return models.KeyValueStore.objects.get(key='payment_gw') 
 
def get_payment_gateway(): 
    payment_config = get_current_gateway().value 
    if payment_config['name'] == 'stripe': 
        return 'stripe' 
    elif payment_config['name'] == 'paypal': 
        return 'PayPal' 
    return 'stripe' 
 
def make_payment(request): 
    # do something related to payment 
    payment_gateway = get_payment_gateway() 
    # process payment 
```

## Configuring Django for production

### Setting up CORS
In settings.py
```python
INSTALLED_APPS = [ 
    ..., 
    "corsheaders", 
    ..., 
] 
```

```python
MIDDLEWARE = [ 
    ..., 
    "corsheaders.middleware.CorsMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    ..., 
] 
```

CORS_ALLOWED_ORIGINS config in the settings.py file:
```python 

CORS_ALLOWED_ORIGINS = [ 
    "https://example.com", 
    "https://sub.example.com", 
    "http://127.0.0.1:9000", 
] 
```

### Exploring WSGI
