# Chapter 1: Setting up Django with DRF

## Table of contents
* [Technical Requirements](#technical-requirements)
* [Why Django?](#why-django)
  * [What is avaiable with Django?](#what-is-avaiable-with-django)
  * [What is the MVT framework?](#what-is-the-mvt-framework)
* [Creating a "Hello World" web app with Django and DRF](#creating-a-hello-world-web-app-with-django-and-drf)
  * [Creating our Django hello_world project](#creating-our-django-hello_world-project)
  * [Creating our first app in Django](#creating-our-first-app-in-django)
  * [Linking app views using urls.py](#linking-app-views-using-urls.py)
  * [Integration DRF](#integration-drf)
* [Creating RESTful API endpoints with DRF](#creating-restful-api-endpoints-with-drf)
  * [Best practices for defining RESTful APIs](#best-practices-for-defining-restful-apis)
  * [Best practices to create a REST API with DRF](#best-practices-to-create-a-rest-api-with-drf)
    * [Using API versioning](#using-api-versioning)
      * [Using a custom version class with DRF](#using-a-custom-version-class-with-drf)
    * [Avoid Router](#avoid-router)
  * [Working with views using DRF](#working-with-views-using-drf)
    * [Functional views](#functional-views)
    * [Class-based views](#class-based-views)
      * [APIView](#apiview)
      * [Generic Views](#generic-views)
* [Introducing API development tools](#introducing-api-development-tools)
  
## Technical Requirements

Learn Django girls tutorial from the official [website](https://tutorial.djangogirls.org/en/)

If you have any doubts about any of the topics mentioned in this or other chapters, feel free to create GitHub issues that specify all the relevant information (https://github.com/PacktPublishing/Django-in-Production/issues) or join our Django in Production Discord channel and ask for any help. 

> [!NOTE]
> 
> Here is the invite link for the Discord server, where you can reach can post any help and also reachout to me directly: https://discord.gg/FCrGUfmDyP.

## Why Django? 

### What is avaiable with Django?

No code applicable to this section

### What is the MVT framework?

Read more about API First developement - https://blog.postman.com/what-is-an-api-first-company/


## Creating a "Hello World" web app with Django and DRF

Using `virtualenv` for creating a virtual environment for our project. (Mac OS X and Linux)

```bash
pip install virtualenv
virtualenv -p python3 v_env
source v_env/bin/activate
```

Using `virtualenv` for creating a virtual environment for our project. (Windows)
Once you download python from the [official website](https://www.python.org/downloads/windows/) , you can use the following command to install virtualenv:

```powershell
py -m pip install --user virtualenv
py -m venv v_env
.\v_env\Scripts\activate
```

Installing Django using pip in the activated virtual environment.
```bash
pip install Django==5.0.1
```

### Creating our Django hello_world project
```bash
mkdir hello_world && cd hello_world
mkdir backend && cd backend
django-admin startproject config .
```
> [!NOTE]
> 
> The `.` at the end of the command is used to create the project in the current directory.

Now run the following command to start the development server:
```bash
python manage.py runserver
```

Open your browser and go to the following URL: http://127.0.0.1:8000/ or http://localhost:8000/ to see the Django welcome page.

Now let us create our first Django `hello_world` view.

Open the `config/urls.py` file and add the following code.

```python
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
def hello_world(request):
    return HttpResponse('hello world')
urlpatterns = [
  path('admin/', admin.site.urls),
  path('hello-world/', hello_world)
]
```

Now go to the following URL: http://127.0.0.1:8000/hello-world/ or http://localhost:8000/hello-world/ to see the `hello world` message.

### Creating our first app in Django

To create our first app in Django, run the following command:

```bash
python manage.py startapp demo_app
```

Now add the newly created app to the `INSTALLED_APPS` list in the `config/settings.py` file.

```python
INSTALLED_APPS = [
    #...
    'django.contrib.staticfiles',
    'demo_app',
]
```

### Linking app views using urls.py

Create a new file `views.py` in the `demo_app` directory and add the following code:

```python
from django.http import HttpResponse

def hello_world(request, *args, **kwargs):
    return HttpResponse('hello world')
```

Create a new file `urls.py` in the `demo_app` directory and add the following code:

```python
from django.urls import path
from demo_app import views

urlpatterns = [
    path('hello-world/', views.hello_world)
]
```

Now link the `demo_app/urls.py` file to the `config/urls.py` file.

```python
from django.contrib import admin
from django.urls import include
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('demo-app/', include('demo_app.urls'))
]
```

When you go to the following URL: http://127.0.0.1:8000/demo-app/hello-world/ or http://localhost:8000/demo-app/hello-world/ you will see the `hello world` message.

### Integration DRF

In order to install Django Rest Framework, we need to install it using pip in the activated virtual environment.

```bash
pip install djangorestframework
```

Now add the newly installed app to the `INSTALLED_APPS` list in the `config/settings.py` file.

```python
DJANGO_APPS = [
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
]

CUSTOM_APPS = [
    'demo_app',
]

INSTALLED_APPS = DJANGO_APPS + CUSTOM_APPS + THIRD_PARTY_APPS
```

Add the following code to the `demo_app/views.py` file.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def hello_world_drf(request, *args, **kwargs):
  return Response(data={'msg':'hello world'})
```

Link the `hello_world_drf` view to the `demo_app/urls.py` file.

```python
from django.urls import path
from demo_app import views

urlpatterns = [
    path('hello-world/', views.hello_world),
    path('hello-world-drf/', views.hello_world_drf)
]
```

To see the `hello world` message in DRF, go to the following URL: http://127.0.0.1:8000/demo-app/hello-world-drf/ or http://localhost:8000/demo-app/hello-world-drf/

## Creating RESTful API endpoints with DRF

### Best practices for defining RESTful APIs

### Best practices to create a REST API with DRF

#### Using API versioning

To enable API versioning with DRF, we need to add the following config in `config/settings.py` file.

```python
REST_FRAMEWORK = {
  'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.URLPathVersioning'
}
```

Add the following code to the `config/urls.py` file.

```python
from django.urls import path
from django.urls import include

urlpatterns = [
  path('<version>/demo-app-version/', include('demo_app.urls'))
]
```

Now add the following code to the `demo_app/views.py` file.

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def demo_version(request, *args, **kwargs):
  version = request.version
  return Response(data={'msg': f'You have hit {version} of demo-api'})
```

Link the `demo_version` view to the `demo_app/urls.py` file.

```python
from django.urls import path
from demo_app import views

urlpatterns = [
    path('hello-world/', views.hello_world),
    path('hello-world-drf/', views.hello_world_drf),
    path('demo-version/', views.demo_version)
]
```

To check the demo version, go to the following URL: http://127.0.0.1:8000/v1/demo-app-version/demo-version/ or http://localhost:8000/v1/demo-app-version/demo-version/

##### Using a custom version class with DRF

Create a new file `custom_versions.py` in the `demo_app` directory and add the following code:

```python
from rest_framework.versioning import URLPathVersioning

class DefaultDemoAppVersion(URLPathVersioning):
    allowed_versions = ['v1']
    version_param = 'version'

class DemoViewVersion(DefaultDemoAppVersion):
    allowed_versions = ['v1', 'v2', 'v3']

class AnotherViewVersion(DefaultDemoAppVersion):
    allowed_versions = ['v1', 'v2']
```

Add the following code to the `demo_app/views.py` file to integrate the custom version class(note that the custom versioning_class can be only linked to a class-based view, so we are  using APIView here):

```python
from rest_framework.response import Response
from rest_framework.views import APIView
from demo_app import custom_versions

class DemoView(APIView):
    versioning_class = custom_versions.DemoViewVersion
    def get(self, request, *args, **kwargs):
        version = request.version
        return Response(data={'msg': f' You have hit {version}'})

class AnotherView(APIView):
    versioning_class = custom_versions.AnotherViewVersion
    def get(self, request, *args, **kwargs):
        version = request.version
        if version == 'v1':
            # perform v1 related tasks
            return Response(data={'msg': 'v1 logic'})
        elif version == 'v2':
            # perform v2 related tasks
            return Response(data={'msg': 'v2 logic'})
```

The final step to  link the `DemoView` and `AnotherView` to the `demo_app/urls.py` file.

```python
from django.urls import path
from demo_app import views

urlpatterns = [
  path('hello-world/', views.hello_world),
  path('demo-version/', views.demo_version),
  path('custom-version/', views.DemoView.as_view()),
  path('another-custom-version/', views.AnotherView.as_view())
]
```

Now to check the custom version, go to the following URL: http://127.0.0.1:8000/v1/demo-app-version/custom-version/ or http://localhost:8000/v1/demo-app-version/custom-version/


#### Avoid Router

No code applicable to this section.

### Working with views using DRF

#### Functional views

Add the following code to the `demo_app/views.py` file.

```python
@api_view(['GET', 'POST', 'PUT'])
def hello_world_functional_view(request, *args, **kwargs):
    if request.method == 'POST':
        return Response(data={'msg': 'POST response block'})
    elif request.method == 'PUT':
        return Response(data={'msg': 'PUT response block'})
    return Response(data={'msg': 'GET response block'})
```


#### Class-based views

##### APIView

Add the following code to the `demo_app/views.py` file.

```python
class DemoAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return Response(data={'msg': 'get request block'})

    def post(self, request, *args, **kwargs):
        return Response(data={'msg': 'post request block'})

    def delete(self, request, *args, **kwargs):
        return Response(data={'msg': 'delete request block'})     
```

To link the DemoAPIView to the `demo_app/urls.py` file, add the following code:

```python
urlpatterns = [
  #...
  path('apiview-class/', views.DemoAPIView.as_view())
]
```

##### Generic Views

No code applicable to this section.

## Introducing API development tools

API development tools are used to test and debug APIs. Some of the popular API development tools are:
- Postman - https://www.postman.com/
- Hoppscotch - https://hoppscotch.io/
- Testmance - https://testmace.com/

Tutorial to learn Postman - https://learning.postman.com/docs/introduction/overview/