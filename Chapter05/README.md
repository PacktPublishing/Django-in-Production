# Mastering Django Authentication and Authorization

## Table of contents

-   [Technical requirements](#technical-requirements)
-   [Learning the basics of Django Authentication](#learning-the-basics-of-django-authentication)
-   [Customizing User model](#customizing-user-model)
-   [Using Django Permissions and Groups](#using-django-permissions-and-groups)
    -   [Using permissions and groups in Django Admin](#using-permissions-and-groups-in-django-admin)
    -   [Creating custom permissions](#creating-custom-permissions)
    -   [Using Django Permissions and Group for API](#using-django-permissions-and-group-for-api)
    -   [Caveats of using permissions](#caveats-of-using-permissions)
-   [Using DRF token-based Authentication](#using-drf-token-based-authentication)
    -   [Integrating Token-Based Authentication in DRF](#integrating-token-based-authentication-in-drf)
    -   [Adding DRF Token based auth to the Django Project](#adding-drftoken-based-auth-to-the-django-project)
    -   [Understanding the limitations of Token-Based Authentication of DRF](#understanding-the-limitations-of-token-based-authentication-of-drf)
-   [Learning about third-party token-based authentication packages](#learning-about-third-party-token-based-authentication-packages)
    -   [django-rest-knox](#django-rest-knox)
    -   [djangorestframework-simplejwt](#djangorestframework-simplejwt)
-   [Integrating Social Login in Django and DRF](#integrating-social-login-in-django-and-drf)

## Technical requirements

## Learning the basics of Django Authentication

Session-based authentication is a vast topic in itself and beyond the scope of this book. If you are not familiar with the session-based authentication concept [Read more on official website](https://docs.djangoproject.com/en/stable/topics/http/sessions/)

## Customizing User model

Custom Model manager from BaseUserManager

```python
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Used for updating default behaviors Django provides
    """

    def create_user(self, phone_no, password, **kwargs):
        # implement create user logic
        user = self.model(phone_no=phone_no, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **kwargs):
        # creates superuser.


class CustomUser(AbstractUser):
    username = None
    phone_no = models.CharField(unique=True, max_length=20)
    city = models.CharField(max_length=40)
    USERNAME_FIELD = "phone_no"
    objects = CustomUserManager()
```

## Using Django Permissions and Groups

### Using permissions and groups in Django Admin

### Creating custom permissions

```python
class Blog(models.Model):
  ...
  class Meta:
    permissions = [
      ("update_title", "Can update the title of the blog"),
      ("update_content", "Can update the content of blog"),
    ]
```

```python
if user.has_perm("blog.update_title"):
   # perform operation
```

### Using Django Permissions and Group for API

```python
def check_permission(user, group_name):
  return user.groups.filter(name=group_name).exists()

@api_view(['POST'])
def comment_view(request):
  if not check_permission(request.user, 'can_comment'):
     return Response(status=403)
  # perform operation
```

For more details, check the official documentation on how to create a custom permission class in DRF [Learn More](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions/)

### Caveats of using permissions

## Using DRF token-based Authentication

### Integrating Token-Based Authentication in DRF

### Adding DRF Token based auth to the Django Project

Django settings to attach the authtoken app to our project

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

We need to add the following configuration to our settings.py to enable authentication and permission to all our views

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
```

permission_classes as AllowAny for our view, or else we will get a 401 error

```python
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
  username = request.DATA['username']
  password = request.DATA['password']
  user = authenticate(username=username, password=password)
  if not user:
    return Response(status='401')
  token = Token.objects.get_or_create(user=user)
  return Response(data={"token": token.key})
```

DRF permission class uses the Django Groups and Permissions framework [More Details](https://www.django-rest-framework.org/api-guide/permissions/#api-reference/)

For the custom Authentication class[follow this link](https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication/)

### Understanding the limitations of Token-Based Authentication of DRF

### Learning about third-party token-based authentication packages

### django-rest-knox

For more details, check the official documentation at [More Details](https://james1345.github.io/django-rest-knox/installation/)

### djangorestframework-simplejwt

The official documentation has detailed instructions on how one can integrate JWT into a Django project [More Details](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)

## Integrating Social Login in Django and DRF

Python Social Auth [More Details](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
