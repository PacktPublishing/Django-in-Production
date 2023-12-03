# Chapter 7: Using Pagination, Django Signals, and Custom Middleware

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

No code applicable to this section

## Paginating Responses in Django and DRF

No code applicable to this section

### Understanding Pagination

No code applicable to this section

### Creating Basic Pagination API in Django

Let us create a simple API that returns a list of all the blogs in the database. Add the following code to the `blog/views.py` file.
```python
# Unpaginated view for blogs returning all the blogs in the database.
@api_view(['GET'])
def get_blog_without_pagination(request):
    blogs = Blog.objects.all()
    blogs_data = BlogSerializer(blogs, many=True).data
    return Response({'blogs': blogs_data})
```

Link the view to the URL `blog/urls.py` file
```python
urlpatterns = [
    path('unpaginated/', views.get_blog_without_pagination),
]
```

Now to test the API, run the server and open the URL `http://127.0.0.1/blog/unpaginated/?page=1&page_size=2`

Now, let us create a paginated view for the blogs. Add the following code to the `blog/views.py` file.
```python
# Paginated view for blogs returning 10 blogs per page.
@api_view(['GET'])
def get_blog_with_pagination(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 10))
    offset = (page-1)*page_size
    limit = page*page_size
    blogs = Blog.objects.all()[offset:limit]
    blogs_data = BlogSerializer(blogs, many=True).data
    return Response({'blogs': blogs_data})
```

Link the view to the URL `blog/urls.py` file
```python
urlpatterns = [
    path('unpaginated/', views.get_blog_without_pagination),
    path('paginated/', views.get_blog_with_pagination),
]
```

Now to test the API, run the server and open the URL `http://127.0.0.1/blog/paginated/?page=1&page_size=2`


### Using Pagination in DRF
> [!NOTE]
> 
> Django provides Paginator class [Read more](https://docs.djangoproject.com/en/stable/topics/pagination/)



> [!NOTE]
> 
> Implementation details of DRF pagination from [the official documentation](https://www.django-rest-framework.org/api-guide/pagination/) 


## Demystifying Django Signals


### Creating custom signals

Create a file `blog/signals.py` and add the following code to it.
```python
from django.dispatch import Signal

notify_author = dispatch.Signal()
```

Now, let us create a receiver for the signal. Add the following code to the `author/receivers.py` file.
```python
from django.dispatch import receiver
from blog.signals import notify_author

@receiver(signals.notify_author)
def send_email_to_author(sender, blog_id, **kwargs):
    # Sends email to author
    print('Sending email to author logic', blog_id, kwargs)
```

Now let us register the receiver. Add the following code to the `blog/apps.py` file.
```python
from django.apps import AppConfig


class AuthorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'author'

    def ready(self):
        from author import receivers
```


Now, let us create a sender for the signal. Add the following code to the `blog/public.py` file.
```python
from blog import signals


def publish_blog(blog_id):
    # publish blog logic to notify author
    signals.notify_author.send(sender=None, blog_id=blog_id)
```

Now, let us create a view to test the signal. Add the following code to the `blog/views.py` file.
```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog import public

# Publish a blog to test the signals.
@api_view(['GET'])
def publish_blog(request):
    blog_id = request.GET.get('id')
    public.publish_blog(blog_id)
    return Response({'status': 'success'})
```

Link the view to the URL `blog/urls.py` file
```python
from django.urls import path

from blog import views


urlpatterns = [
    path('publish/', views.publish_blog),
]
```

Now to test the API, run the server and open the URL `http://127.0.0.1/blog/publish/?id=1` and check the console for the output. You should see the following output.
```
Sending email to author logic 1 {}
```

### Working with signals in production

No code applicable to this section

## Working with Django Middleware

Django default `MIDDLEWARE` value in `setting.py` file
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

Create `common/custom_middleware.py` file and add the following code to it.
```python
class CustomMiddleware: 
    def __init__(self, get_response): 
      self.get_response = get_response 
 
    def __call__(self, request): 
      print("custom middleware before request view") 
      # Code to be executed for each request before 
      # the view (and later middleware) are called. 
      response = self.get_response(request) 
      
      # Code to be executed for each response after the view is called 
      print("custom middleware after response view") 
      return response 
```

middleware configuration in settings.py
```python
MIDDLEWARE = [
    . . .  
    # Custom middleware 
    "common.custom_middleware.CustomMiddleware", 
] 
```

Now to test the integration of middleware, run the server and open any URl in the browser. You should see the following output in the console.
```
custom middleware before request view
custom middleware after response view
[15/Jul/2021 12:00:00] "GET / HTTP/1.1" 200 16348
```
