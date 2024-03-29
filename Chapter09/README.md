# Chapter 9: Writing Tests in Django

## Table of contents
* [Technical requirements](#technical-requirements)
* [Introducing the different types of tests in Software software Development](#introducing-the-different-types-of-tests-in-software-software-development)
    * [Unit testing](#unit-testing)
    * [Integration testing ](#integration-testing)
    * [E2E testing](#e2e-testing)
* [Setting up tests for Django and DRF](#setting-up-tests-for-django-and-drf)
    * [Structuring and Naming test](#structuring-and-naming-test)
    * [Setting up a database for tests](#setting-up-a-database-for-tests)
    * [Writing basic tests in DRF](#writing-basic-tests-in-drf)
    * [Writing tests for advance use cases](#writing-tests-for-advance-use-cases)
        * [Testing API Authentication](#testing-api-authentication)
        * [Setting up and tearing down test cases](#setting-up-and-tearing-down-test-cases)
        * [Using Factoryboy](#using-factoryboy)
        * [Using setUpTestData](#using-setuptestdata)
        * [Using mocks as less as possible](#using-mocks-as-less-as-possible)
        * [Writing tests for Celery](#writing-tests-for-celery)
        * [Writing tests for Signals and Receivers](#writing-tests-for-signals-and-receivers)
    * [Using custom Django Runners](#using-custom-django-runners)
* [Learning the best practices to write tests](#learning-the-best-practices-to-write-tests)
    * [Using unit tests more often](#using-unit-tests-more-often)
    * [Writing tests for advance use cases](#writing-tests-for-advance-use-cases)
    * [Avoiding time bomb test failures](#avoiding-time-bomb-test-failures)
    * [Avoiding brittle tests](#avoiding-brittle-tests)
    * [Using a reverse function for URL path in tests](#using-a-reverse-function-for-url-path-in-tests)
    * [Using Authentication tests](#using-authentication-tests)
    * [Using test tags to group tests](#using-test-tags-to-group-tests)
    * [Using Postman to create an integration test suite](#using-postman-to-create-an-integration-test-suite)
    * [Creating different types of tests](#creating-different-types-of-tests)
    * [Avoiding tests](#avoiding-tests)
* [Exploring Testtest-Driven Development (TDD)](#exploring-testtest-driven-development-tdd)


## Technical requirements

> [!NOTE]
> 
> Join the Discord server "[Django in Production](https://discord.gg/FCrGUfmDyP)" for direct support from the author as you follow the instructions in the book. Feel free to reach out for any help or clarifications needed. https://discord.gg/FCrGUfmDyP.


## Introducing the different types of tests in Software software Development

No code applicable to this section

### Unit testing

No code applicable to this section

### Integration testing

No code applicable to this section

### E2E testing

[Writing E2E test with postman](https://learning.postman.com/docs/writing-scripts/test-scripts/)
[Playwright](https://playwright.dev/)
[Puppeteer](https://pptr.dev/)

## Setting up tests for Django and DRF
unittest [Read more](https://docs.djangoproject.com/en/stable/topics/testing/)

pytest-django [Read more](https://pytest-django.readthedocs.io/en/latest/)

### Structuring and Naming test

No code applicable to this section

### Setting up a database for tests

To setup a database for tests we can use the following configuration in the `settings.py` file.

Add the `TEST` key in the `DATABASES` config in the `settings.py`. The `TEST` key would be used to create a separate database for tests, `NAME` is the name of the database that would be created for tests.

```python
DATABASES = { 
    "default": { 
        "ENGINE": "django.db.backends.postgresql", 
        "USER": "mydatabaseuser", 
        "NAME": "mydatabase", 
        "TEST": { 
            "NAME": "mytestdatabase", 
        }, 
    }, 
} 
```
> [!CAUTION]
> 
> If you are using [ElephantSQL](https://www.elephantsql.com/) as your database provider then you might get errors while running tests. 
> To fix this issue you can use [Neon](https://neon.tech) as your database provider, Neon is a postgres fork that is compatible with Postgres. Please note use Neon only for testing purposes and in this chapter only, do not use it in production unless you are confident on it.

### Writing basic tests in DRF

Add the following code in the `blog/views.py` file
```python
from rest_framework import status 
from rest_framework.decorators import api_view 
from rest_framework.response import Response 
 
@api_view(['GET']) 
def basic_req(request): 
    if request.method == 'GET': 
        resp = {"msg": "hello world!"} 
        return Response(data=resp, status=status.HTTP_200_OK) 
```
Link the view in the `blog/urls.py` file

```python
from django.urls import path
from blog import views

urlpatterns = [
    path('hello-world/', views.basic_req, name='basic-req'),
]
```

Using DRF’s default testing framework to write tests. 

Add the following code in the `blog/tests.py` file
```python
from rest_framework.test import APITestCase 
from rest_framework import status 
 
class BasicTests(APITestCase): 
    def test_basic_req(self): 
        """ 
        Test the basic url path response. 
        """ 
        # ARRANGE - Create a reverse URL and the expected response. 
        url = '/blog/hello-world/' 
        expected_data = {"msg": "hello world!"} 
 
        # ACT – Perform API call by DRF’s test APIClient. 
        response = self.client.get(url, format='json')  

        # ASSERT- Verify the response. 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data, expected_data) 
```

Run the test using the following command and you should see the following output : 
```bash
> python manage.py test

Found 1 test(s).
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
custom middleware before request view
custom middleware after response view
.
----------------------------------------------------------------------
Ran 1 test in 0.369s

OK
Destroying test database for alias 'default'...
```

### Writing tests for advance use cases

#### Testing API Authentication

To test Authentication we need to enable the authentication in our view. We can use the following code in the `blog/views.py` file
```python
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def hello_world_2(request):
    resp = {"msg": "hello world!"}
    return Response(data=resp, status=status.HTTP_200_OK)
```


Now let us update our test case to use the authentication token. We can use the following code in the `blog/tests.py` file

```python
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
class BasicTests2(APITestCase):
    def test_unauthenticated_req(self):
        url = '/blog/hello-world-2/'
        response = self.client.get(url, format='json')

        # Since the user is not logged in it would get 401.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_authenticated_req(self):
        url = '/blog/hello-world-2/'
        expected_data = {"msg": "hello world!"}
        # Create a user and get the token. This is important.
        user = User.objects.create_user(username='demouser', password='demopass')
        token, created = Token.objects.get_or_create(user=user)

        # Login to the request using the HTTP header token.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')
        response = self.client.get(url, format='json')

        # User is logged in we would get the expected 200 response code.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

    def test_wrong_authenticated_req(self):
        url = '/blog/hello-world-2/'

        # Login to the request using a random wrong token.
        self.client.credentials(HTTP_AUTHORIZATION=f'Token random')
        response = self.client.get(url, format='json')

        # Request has the wrong token so it would get 401.
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_force_authenticate_with_user(self):
        """
        Setting `.force_authenticate()` with a user forcibly authenticates.
        """
        u1 = User.objects.create_user('a1', 'a1@abc.co')
        url = '/blog/hello-world/'
    
        # Forcefully login and update request.user
        self.client.force_authenticate(user=u1)
        response = self.client.get(url)
        expected_data = {"msg": "hello world!"}
        # Tests work with the login user.
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, expected_data)

```

#### Setting up and tearing down test cases

```python
class BasicTests3(APITestCase): 
     
    def setUp(self): 
        self.test_url = reverse('basic-req') 
        user = User.objects.create_user('a1', 'a1@abc.co') 
        self.client.force_authenticate(user=user) 
        print('Running Setup') 
         
    def test_with_setup_authenticated_req(self): 
        print('test 1 running') 
        expected_data = {"msg": "hello world!"}         
        response = self.client.get(self.url, format='json') 
 
        # User is logged in, expected 200 response code. 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data, expected_data) 
 
    # demo test 
    def test_demo(self): 
        print('test 2 running') 
        self.assertEqual(1,1) 
 
    def tearDown(self): 
        self.client.logout() 
        print('Running teardown') 
```

#### Using Factoryboy

To use factoryboy we need to install it using the following command
```bash
pip install factory-boy

Create a new file `blog/factoryboy.py` and add the following code in it.
```python
from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory

from blog import models as blog_models
from author import models as author_models


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = author_models.Author

    name = Sequence(lambda n: f'Author {n}')
    email = Sequence(lambda n: f'a{n}@gmail.com')


class CoverImageFactory(DjangoModelFactory):
    class Meta:
        model = blog_models.CoverImage

    image_link = Sequence(lambda n: f'https://www.example.com/image/{n}')


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = blog_models.Blog

    title = Sequence(lambda n: f'Blog {n}')
    content = Sequence(lambda n: f'Blog content {n}')
    author = SubFactory(AuthorFactory)
    cover_image = SubFactory(CoverImageFactory)
```


Now we can use the factory to create test data in our test cases. We can use the following code in the `blog/tests.py` file

```python

from blog.factoryboy import BlogFactory
class BlogTestCase4(APITestCase): 
 
    def test_total_blogs(self):
        blogs = BlogFactory.create_batch(4)
        url = '/blog/unpaginated/'
        
        resp = self.client.get(url, format='json')

        self.assertEqual(len(resp.data['blogs']), 4)
 
```

Read more about factoryboy from the official documentation -: [Link](https://factoryboy.readthedocs.io/en/stable/orms.html)

#### Using setUpTestData

Example using only setUp
```python
class BlogTestCase5(APITestCase):
    def setUp(self):
        self.blog = BlogFactory(title='a1', content='a b c')
        print('Running Setup multiple times')

    def test_word_count_1(self):
        expected_count = 3
        print('test_word_count_1 running')
        self.assertEqual(expected_count, 3)

    def test_title_length_1(self):
        expected_length = 2
        print('test_title_length_1 running')
        self.assertEqual(expected_length, 2) 
```

Example using `setUpTestData` 
```python
class BlogTestCase6(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.blog = BlogFactory(title='a1', content='a b c')
        print('Running Setup only once')

    def test_word_count_2(self):
        expected_count = 3
        print('test_word_count_2 running')
        self.assertEqual(expected_count, 3)

    def test_title_length_2(self):
        expected_length = 2
        print('test_title_length_2 running')
        self.assertEqual(expected_length, 2) 
```

Read more about `setUpTestData` from the official documentation -: [Link](https://docs.djangoproject.com/en/stable/topics/testing/tools/#django.test.TestCase.setUpTestData)

#### Using mocks as less as possible

[Youtube Link](https://www.youtube.com/watch?v=ww1UsGZV8fQ): – Explains what goes under the hood when we patch a function while writing tests. 

[Youtube Link](https://www.youtube.com/watch?v=rk-f3B-eMkI): – Explains how we can stop using mocks that can help us rethink the way we write application code that is well designed. 

[Youtube Link](https://www.youtube.com/watch?v=Ldlz4V-UCFw): – Explains different approaches to writing tests without over-using mocks. 

#### Writing tests for Celery


#### Writing tests for Signals and Receivers

Write a signal in the `author/signals.py` file
```python
from django.db.models.signals import post_save 
from django.dispatch import receiver
from author.models import Author 
 
@receiver(post_save, sender=Author) 
def my_handler(sender, **kwargs): 
    print("Signal called")
```

Add the following code in the `author/tests/tests_signals.py` file
```python
from django.test import TestCase
from django.db.models import signals

from author.models import Author
from author.receivers import my_handler


class SignalsTest(TestCase):
    def test_connection(self):
        result = signals.post_save.disconnect(
           receiver=my_handler, sender=Author
        )
        self.assertTrue(result) 
```

Read more about the disconnect function from Django official documentation -: [Link](https://docs.djangoproject.com/en/stable/topics/signals/#disconnecting-signals)


Factoryboy also gives a way to mute signals. We can use the following code in the `author/tests/tests_signals.py` file
```python
from factory.django import mute_signals  
 
class SignalsTest(TestCase): 
 
    def test_demo(self): 
        with mute_signals(signals.pre_save, signals.post_save): 
            # pre_save/post_save won't be called here. 
            return BlogFactory(), AuthorFactory() 
```
Read more on how we can use factoryboy to mute signals and have faster test execution. [Link](https://factoryboy.readthedocs.io/en/stable/orms.html#factory.django.mute_signals)

### Using custom Django Runners

Django’s default runner DiscoverRunner

Create a new file `common/custom_runner.py` and add the following code in it.
```python
from django.test.runner import DiscoverRunner 
 
class FillData: 
    def setup_databases(self, *args, **kwargs): 
        temp = super(FillData, self).setup_databases(*args, **kwargs) 
        print("### Populating Test Cases Database ###") 
        # Create any data 
        print("### Database populated ############") 
        return temp 
 
class CustomRunner(FillData, DiscoverRunner): 
    pass 
```

Now add the custom runner in the `settings.py` file
```python
TEST_RUNNER = 'common.custom_runner.CustomRunner'
```

Now run the tests using the following command and you should see the following output
```bash
> python manage.py test

### Populating Test Cases Database ###
### Database populated ############
Creating test database for alias 'default'...
...
```

For more details on how to write custom runners please refer to the official documentation -: [Link](https://docs.djangoproject.com/en/stable/topics/testing/advanced/#defining-a-test-runner)

## Learning the best practices to write tests

### Using unit tests more often

### Writing tests for advance use cases

### Avoiding time bomb test failures

Install freezegun using the following command
```bash
pip install freezegun
```
To test freezegun we can assume the following condition. A user can post only 10 blogs per day.

Let us create a new file `blog/public.py` and add the following code in it
```python
from django.utils import timezone

from blog.models import Blog


def check_if_allowed_to_publish_blog(author):
    # check if author is allowed to publish blog
    blog_count_for_today = Blog.objects.filter(author_id=author.id, created_at__date=timezone.now().date()).count()
    return blog_count_for_today < 10
```

Now use the following code in the `blog/tests.py` file

```python
from django.utils import timezone 
from freezegun import freeze_time

from blog.factoryboy import BlogFactory, AuthorFactory
from blog import public

class BlogTests7(APITestCase):
    def test_blog_time_block(self):
        today = timezone.now().date()
        tomo = timezone.now().date() + timezone.timedelta(days=1)

        with freeze_time(today) as frozentime:
            # Post 10 blogs
            author = AuthorFactory()
            create_10_blogs = BlogFactory.create_batch(10, author=author)
            # Check if the user can post more blogs today
            user_can_post = public.check_if_allowed_to_publish_blog(author)
            # Validate that the user cannot post a blog today.
            self.assertFalse(user_can_post)

            # Move the date to the next day
            frozentime.move_to(tomo)
            # Validate that the user cannot post a blog tomorrow.
            result = public.check_if_allowed_to_publish_blog(author)
            self.assertTrue(result)
```

### Avoiding brittle tests

### Using a reverse function for URL path in tests

### Using Authentication tests

### Using test tags to group tests

```python
from django.test import tag
from rest_framework.test import APITestCase
 
class BlogTests8(APITestCase):
    @tag("fast")
    def test_fast(self):
        print("fast test running")

    @tag("slow")
    def test_slow(self):
        print("slow test running")

    @tag("slow", "core")
    def test_slow_but_core(self):
        print("slow but core test running")
```

To run the tests with tag `core` we can use the following command -: 
```bash
python manage.py test --tag=core
```

[Read more](https://docs.djangoproject.com/en/stable/topics/testing/tools/#tagging-tests)

### Using Postman to create an integration test suite

How to write test scripts in Postman -: [Link](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/)

How to create Monitors monitors that would will periodically check for the tests to pass -: Link](https://learning.postman.com/docs/monitoring-your-api/intro-monitors/)

How to use the postman Postman cli CLI to run test cases from the CI/CD pipeline - Link](https://learning.postman.com/docs/postman-cli/postman-cli-overview/)

### Creating different types of tests

No code applicable to this section

### Avoiding tests

No code applicable to this section

## Exploring Testtest-Driven Development (TDD)

[More Resource](https://www.packtpub.com/product/hands-on-test-driven-development-with-python-video/9781789138313)


