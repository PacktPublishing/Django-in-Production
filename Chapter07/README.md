# Using Pagination, Django Signals, and Custom Middleware

## Table of contents
* [Technical requirements](#technical-requirements)
* [Paginating Responses in Django and DRF](#paginating-responses-in-django-and-drf)
  * [Understanding Pagination](#understanding-pagination)
  * [Using Pagination in DRF](#using-pagination-in-drf)
* [Demystifying Django Signals](#demystifying-django-signals)
  * [Creating custom signals](#creating-custom-signals)
  * [Working with signals in production](#working-with-signals-in-production)
* [Working with Django Middleware](#working-with-django-middleware)
* [Creating Custom Middleware](#creating-custom-middleware)


## Technical requirements


## Paginating Responses in Django and DRF

### Understanding Pagination


### Using Pagination in DRF
Django provides Paginator class [Read more](https://docs.djangoproject.com/en/stable/topics/pagination/)

Implementation details from the official documentation [Read more](https://www.django-rest-framework.org/api-guide/pagination/) 


## Demystifying Django Signals


### Creating custom signals


### Working with signals in production


## Working with Django Middleware

MIDDLEWARE setting.
```python
MIDDLEWARE = [ 
    "django.middleware.security.SecurityMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware", 
    "django.contrib.messages.middleware.MessageMiddleware", 
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
] 
```


## Creating Custom Middleware

code in the custom_middleware.py
```python
class CustomMiddleware: 
    def __init__(self, get_response): 
      self.get_response = get_response 
 
    def __call__(self, request): 
      print("custom middleware before next middleware/view") 
      # Code to be executed for each request before 

      # the view (and later middleware) are called. 
      response = self.get_response(request) 
      # Code to be executed for each response after the view is called 
      print("custom middleware after response or previous middleware") 
      return response 
```

middleware configuration in settings.py
```python
MIDDLEWARE = [ 
    "django.middleware.security.SecurityMiddleware", 
    "django.contrib.sessions.middleware.SessionMiddleware", 
    "django.middleware.common.CommonMiddleware", 
    "django.middleware.csrf.CsrfViewMiddleware", 
    "django.contrib.auth.middleware.AuthenticationMiddleware", 
    "django.contrib.messages.middleware.MessageMiddleware", 
    "django.middleware.clickjacking.XFrameOptionsMiddleware", 
    # Custom middleware 
    "custom_middleware.CustomMiddleware", 
] 
```

