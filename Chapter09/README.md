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


## Introducing the different types of tests in Software software Development

### Unit testing

### Integration testing

### E2E testing

## Setting up tests for Django and DRF
unittest [Read more](https://docs.djangoproject.com/en/stable/topics/testing/)

pytest-django [Read more](https://pytest-django.readthedocs.io/en/latest/)

### Structuring and Naming test

### Setting up a database for tests
NAME config inside the TEST attribute
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

### Writing basic tests in DRF

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

 DRF’s default testing framework to write tests
```python
from django.urls import reverse 
from rest_framework.test import APITestCase 
from rest_framework import status 
 
class BasicTests(APITestCase): 
    def test_basic_req(self): 
        """ 
        Test the basic url path response. 
        """ 
        # ARRANGE - Create a reverse URL and the expected response. 
        url = reverse('basic-req')  
        expected_data = {"msg": "hello world!"} 
 
        # ACT – Perform API call by DRF’s test APIClient. 
        response = self.client.get(url, format='json')  

        # ASSERT- Verify the response. 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data, expected_data) 
```

### Writing tests for advance use cases

#### Testing API Authentication

```python
class BasicTests(APITestCase): 
    def test_unauthenticated_req(self): 
        url = reverse('basic-req') 
        response = self.client.get(url, format='json') 
 
        # Since the user is not logged in it would get 401. 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) 
 
    def test_authenticated_req(self): 
        url = reverse('basic-req') 
        expected_data = {"msg": "hello world!"} 
        token = Token.objects.get(user__username='demouser').key 
 
        # Login to the request using the HTTP header token. 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}') 
        response = self.client.get(url, format='json') 
 
        # User is logged in we would get the expected 200 response code. 
        self.assertEqual(response.status_code, status.HTTP_200_OK) 
        self.assertEqual(response.data, expected_data) 
 

    def test_wrong_authenticated_req(self): 
        url = reverse('basic-req') 
     
        # Login to the request using a random wrong token. 
        self.client.credentials(HTTP_AUTHORIZATION=f'Token random') 
        response = self.client.get(url, format='json') 
 
        # Request has the wrong token so it would get 401. 
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
```

#### Setting up and tearing down test cases

```python
class BasicTests(APITestCase): 
     
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

```python
from factory import SubFactory, Sequence 
from factory.django import DjangoModelFactory 
 
from blog import models as blog_models 
from author import models as author_models 
 
class AuthorFactory(DjangoModelFactory): 
    class Meta: 
        model = author_models.Author 
    name = Sequence(lambda n: f'Author {n}') 
 
 
class BlogFactory(DjangoModelFactory): 
    class Meta: 
        model = blog_models.Blog 
    title = Sequence(lambda n: f'Blog {n}') 
    author = SubFactory(AuthorFactory) 
```

```python
class BlogTestCase(APITestCase): 
 
    def test_total_blogs(self): 
        blogs = BlogFactory.create_batch(4) 
        url = reverse('blog-list') 
         
        resp = self.client.get(url, format='json') 
 
        self.assertEqual(len(resp['data']), 4) 
```

#### Using setUpTestData

```python
class BlogTestCase(APITestCase): 
    def setUp(self): 
        self.blog = BlogFactory(title='a1', content='a b c') 
     
    def test_word_count(self): 
        expected_count = 3 
        actual_count = public.count_word(self.blog) 
        self.assertEqual(expected_count, actual_count) 
         
    def test_title_length(self): 
        expected_length = 2 
        actual_length = public.calculate_length(self.blog) 
        self.assertEqual(expected_length, actual_length) 
```

```python
class BlogTestCase(APITestCase): 
    @classmethod 
    def setUpTestData(cls): 
        cls.blog = BlogFactory(title='a1', content='a b c') 
 
    def test_word_count(self): 
        expected_count = 3 
        actual_count = public.count_word(self.blog) 
        self.assertEqual(expected_count, actual_count) 
 
    def test_title_length(self): 
        expected_length = 2 
        actual_length = public.calculate_length(self.blog) 
        self.assertEqual(expected_length, actual_length) 
```

#### Using mocks as less as possible

[Youtube Link](https://www.youtube.com/watch?v=ww1UsGZV8fQ): – Explains what goes under the hood when we patch a function while writing tests. 

[Youtube Link](https://www.youtube.com/watch?v=rk-f3B-eMkI): – Explains how we can stop using mocks that can help us rethink the way we write application code that is well designed. 

[Youtube Link](https://www.youtube.com/watch?v=Ldlz4V-UCFw): – Explains different approaches to writing tests without over-using mocks. 

#### Writing tests for Celery

```python
from django.db.models.signals import pre_save 
from django.dispatch import receiver 
from myapp.models import MyModel 
 
@receiver(pre_save, sender=MyModel) 
def my_handler(sender, **kwargs): 
    ... 
```

```python
class SignalsTest(TestCase): 
    def test_connection(self): 
        result = signals.post_save.disconnect( 
           receiver=my_handler, sender=MyModel 
        ) 
        self.assertTrue(result) 
```

Read more about the disconnect function from Django official documentation -: [Link](https://docs.djangoproject.com/en/stable/topics/signals/#disconnecting-signals)

#### Writing tests for Signals and Receivers

```python
from factory.django import mute_signals  
 
class SignalsTest(TestCase): 
 
    def test_demo(self): 
        with mute_signals(signals.pre_save, signals.post_save): 
            # pre_save/post_save won't be called here. 
            return SomeFactory(), SomeOtherFactory() 
```
Read more on how we can use factoryboy to mute signals and have faster test execution. [Link](https://factoryboy.readthedocs.io/en/stable/orms.html#factory.django.mute_signals)

### Using custom Django Runners

Django’s default runner DiscoverRunner
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

## Learning the best practices to write tests

### Using unit tests more often

### Writing tests for advance use cases

### Avoiding time bomb test failures

```python
from django.test import TestCase 
from django.utils import timzone 
from freezegun import freeze_time 
 
class CommentTests(APITestCase): 
    def test_comment_block(self): 
        today = timezone.now().date() 
        tomo = timezone.now().date() + timzone.timedelta(days=1) 
 
        with freeze_time(today) as frozentime: 
            # Post 10 comments on users 
            action = post_10_comments(comment_list) 
            # Check if the user can post more comments today 
            result = check_user_can_post(user) 
            # Validate that the user cannot post a comment today. 
            self.assertFalse(result) 
 
            # Move the date to the next day 
            frozentime.move_to(tomo) 
            result = check_user_can_post() 
            self.assertTrue(result)            
```

### Avoiding brittle tests

### Using a reverse function for URL path in tests

### Using Authentication tests

### Using test tags to group tests

```python
from django.test import tag 
 
class SampleTestCase(APITestCase): 
    @tag("fast") 
    def test_fast(self): 
        ... 
 
    @tag("slow") 
    def test_slow(self): 
        ... 
 
    @tag("slow", "core") 
    def test_slow_but_core(self): 
        ... 
```
[Read more](https://docs.djangoproject.com/en/stable/topics/testing/tools/#tagging-tests)

### Using Postman to create an integration test suite

How to write test scripts in Postman -: [Link](https://learning.postman.com/docs/writing-scripts/script-references/test-examples/)

How to create Monitors monitors that would will periodically check for the tests to pass -: Link](https://learning.postman.com/docs/monitoring-your-api/intro-monitors/)

How to use the postman Postman cli CLI to run test cases from the CI/CD pipeline - Link](https://learning.postman.com/docs/postman-cli/postman-cli-overview/)

### Creating different types of tests

### Avoiding tests

## Exploring Testtest-Driven Development (TDD)

[More Resource](https://www.packtpub.com/product/hands-on-test-driven-development-with-python-video/9781789138313)


