# Chapter 5: Mastering Django Authentication and Authorization

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

No code applicable to this section

## Learning the basics of Django Authentication

No code applicable to this section

> [!NOTE]
> 
> Session-based authentication is a vast topic in itself and beyond the scope of this book. If you are not familiar with the session-based authentication concept [Read more on official website](https://docs.djangoproject.com/en/stable/topics/http/sessions/)

## Customizing User model

Custom Model manager from BaseUserManager

Create a new app called `custom_user` using the following command

```bash
python manage.py startapp custom_user
```

Define a custom user model in the `custom_user/models.py` file
```python
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUserManager(BaseUserManager):
    """
    Used for updating default behaviour Django provides
    """

    def create_user(self, phone_no, password, **kwargs):
        # implement create user logic
        user = self.model(phone_no=phone_no, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_no, password, **kwargs):
        # creates superuser.
        user = self.create_user(phone_no, password, **kwargs)
        return user


class CustomUser(AbstractUser):
    username = None
    phone_no = models.CharField(unique=True, max_length=20)
    city = models.CharField(max_length=40)
    USERNAME_FIELD = "phone_no"
    objects = CustomUserManager()
```

Now we need to update the `settings.py` file to use our custom user model

```python
AUTH_USER_MODEL = 'accounts.CustomUser'
```

> [!NOTE]
> 
> If you are using custom user model, you need to create a new database and run migrations. If you use it with existing database you will get errors.

Now run the migration for the new model

```bash
python manage.py makemigrations
python manage.py migrate
```

> [!NOTE]
> To use custom use model in Django [Please Read more on official website](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model)

## Using OneToOneField relationship with user model

To use OneToOneField relationship with user model, we need to create a new model and add a OneToOneField relationship with the user model

Create a new app called `user_profile` using the following command

```bash
python manage.py startapp custom_user
``` 

Define a new model in the `user_profile/models.py` file

```python
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', related_name='user_profile', on_delete=models.CASCADE)
    phone_no = models.CharField(unique=True, max_length=20)
    city = models.CharField(max_length=40)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
```

Now run the migration for the new model

```bash
python manage.py makemigrations
python manage.py migrate
```

## Using Django Permissions and Groups

No code applicable to this section

### Using permissions and groups in Django Admin

No code applicable to this section

### Creating custom permissions

Create a custom permission in the `blog/models.py` file to allow only certain users update the title and content of the blog. 

```python
from django.db import models

class Blog(models.Model):
  ...
  class Meta:
    permissions = [
      ("update_title", "Can update the title of the blog"),
      ("update_content", "Can update the content of blog"),
    ]
```

Now we need to run the migration for the new permission

```bash
python manage.py makemigrations
python manage.py migrate
```

Now we can use the permission in our code as follows
```python
def update_blog_title(request):
    blog_id = request.GET.get('id')
    blog = Blog.objects.get(id=blog_id)
    if request.user.has_perm("blog.update_title"):
        # perform operation
        return HttpResponse('User has permission to update title')
    return HttpResponse('User does not have permission to update title')
```

> [!NOTE]
> 
> If you are logged into Django admin interface as a superuser, then you would always see User has permission to update title. This happens because in Django super user has access to all the permissions implicitly. But not every staff user has site wide permission, so one should create a normal staff user and assign custom permission to test the code.


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

No code applicable to this section

## Using DRF token-based Authentication

No code applicable to this section

### Integrating Token-Based Authentication in DRF

No code applicable to this section

### Adding DRF Token based auth to the Django Project

Go to Django `settings.py` to attach the `rest_framework.authtoken` app to our project

```python
INSTALLED_APPS = [
    ...
    'rest_framework.authtoken'
]
```

Now we need to run the migration for the `authtoken` to be available. 

```bash
python manage.py migrate
```
In order to enable authentication and permission to all our views.
We need to add the following configuration to our `settings.py` file

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

Create a login view in the `custom_user/views.py` file

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
Use `permission_classes` as `AllowAny` for our `login` view, or else we will get a 401 error.

Now link the `login` view to the `custom_user/urls.py` file

```python
urlpatterns = [
    ...
    path('login/', views.login),
]
```

Also do not forget to link the `custom_user/urls.py` file to the `config/urls.py` file

```python
urlpatterns = [
    ...
    path('api/auth/v1/', include('custom_user.urls')),
]
```

We can test our login view using the browser and going to the following URL and passing the username and password as form data

```bash
http://127.0.0.1:8000/api/auth/v1/login/
```

> [!NOTE]
> 
> DRF permission class uses the Django Groups and Permissions framework [More Details](https://www.django-rest-framework.org/api-guide/permissions/#api-reference/)
> For the custom Authentication class [follow this link](https://www.django-rest-framework.org/api-guide/authentication/#custom-authentication/)

### Understanding the limitations of Token-Based Authentication of DRF

No code applicable to this section

## Learning about third-party token-based authentication packages

No code applicable to this section

### django-rest-knox

For more details, check the official documentation at [More Details](https://james1345.github.io/django-rest-knox/installation/)

### djangorestframework-simplejwt

The official documentation has detailed instructions on how one can integrate JWT into a Django project [More Details](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/getting_started.html)

## Integrating Social Login in Django and DRF

Python Social Auth [More Details](https://python-social-auth.readthedocs.io/en/latest/configuration/django.html)
