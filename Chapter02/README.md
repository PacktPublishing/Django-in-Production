# Chapter 2 Exploring Django ORM, Models and Migrations

## Table of contents
* [Setting up postgreSQL with Django Project](#setting-up-postgresql-with-django-project)
  * [Configuring Django with PostgreSQL](#configuring-django-with-postgresql)
* [Using Models and Django ORM](#using-models-and-django-orm)
  * [Basic ORM concepts](#basic-orm-concepts)
* [Understanding the crux of Django Migration](#understanding-the-crux-of-django-migration)
  * [Performing DB migrations like a pro](#performing-db-migrations-like-a-pro)
    * [Use Fake migration](#use-fake-migration)
* [Learning about Performance Optimization](#learning-about-performance-optimization)
  * [Understanding Django ORM like a pro](#understanding-django-orm-like-a-pro)
    * [Using select_related and prefetch_related](#using-select_related-and-prefetch_related)


## Setting up postgreSQL with Django Project

### Configuring Django with PostgreSQL

Install psycopg2-binary using pip in the activated virtual environment.

```bash
pip install psycopg2-binary
```

Replace the default database configuration in the settings.py file with the following:

Your current database configuration should be connecting to SQLite3. And the settings files should looks something like this

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Now, we need to change the database configuration to connect to PostgreSQL. The settings file should look something like this:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "tiny.db.elephantsql.com",
        "NAME": "wcgzvqra",
        "USER": "wcgzvqra",
        "PORT": 5432,
        "PASSWORD": "lyuX6vWvAtrqZSY1oiPKNBMoKFkctBVn",
    }
}
```
Please note that the above configuration is for connecting to the PostgreSQL database hosted on [ElephantSQL](https://www.elephantsql.com/). You can create a free account on ElephantSQL and create a database instance. Once you create a database instance, you can get the connection details from the dashboard. And the credentials used above are just for demonstration purposes. You can use the credentials from your database instance.

## Using Models and Django ORM

### Adding Django models
Create new django apps using the following command:

```bash
python manage.py startapp author
python manage.py startapp blog
```

Add the newly created apps to the INSTALLED_APPS list in the settings.py file.

```python
CUSTOM_APPS = [
    "author",
    "blog",
]
```

Create a new model in the author/models.py file.

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    bio = models.TextField()

    def __str__(self):
        return self.name

```

create a new model in the blog/models.py file.

```python
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey('author.Author', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```

Creating migrations

```bash
python manage.py makemigrations
```

Running migrations

```bash
python manage.py migrate
```


### Basic ORM concepts

To follow along the examples, you need to have dummy data in the database. You can create dummy data using the following command:

```bash
python manage.py shell < helper/create_dummy_data_02_01.py
```

you can use the Django shell. You can start the Django shell using the following command:

```bash
python manage.py shell
```

## Understanding the crux of Django Migration

### Performing DB migrations like a pro

#### Use Fake migration

In order to use fake migration, we need to create a db change that can be faked. For example, we can add a new field to the Author model.

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    demo_field = models.TextField(default='demo') # Uncomment this line to test fake migrations
    email = models.EmailField(unique=True)
    bio = models.TextField()

    def __str__(self):
        return self.name
```

now run the following commands:

```bash
python manage.py makemigrations
python manage.py migrate author 0002 --fake
```
We have now faked the migration. Now, if we run the migrate command again, it will not apply the migration.

```bash
python manage.py migrate
```

Now to revert the fake migrations 

```bash
python manage.py migrate author 0001 --fake
```
## Learning about Performance Optimization

### Understanding Django ORM like a pro

#### Using select_related and prefetch_related

To understand the advantage of using select_related and prefetch_related, we need to understand the concept of database joins. And also how Django ORM works using the hood when we have multiple queries.

First we need to create a decorator that we can use to measure the queries used when querying.

```python
from django.db import connection
from django.db import reset_queries

def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func()
        query_info = connection.queries
        print(f'function_name: {func.__name__}')
        print(f'query_count: {len(query_info)}')
        queries = [f'{ query["sql"]}\n' for query in query_info]
        print(f'queries: \n{"".join(queries)}')
        return results
    return inner_func
```

Now we can use the decorator to measure the queries used when querying.

```python
from author import models

@database_debug
def regular_query():
    blogs = models.Blog.objects.all()
    return [blog.author.first_name for blog in blogs]

regular_query()

##################
OUTPUT Result

function_name: regular_query
query_count: 4
queries:
SELECT "blog_blog"."id", "blog_blog"."title", "blog_blog"."content", "blog_blog"."author_id", "blog_blog"."created_at", "blog_blog"."updated_at" FROM "blog_blog"
SELECT "author_author"."id", "author_author"."name", "author_author"."email", "author_author"."bio" FROM "author_author" WHERE "author_author"."id" = 1 LIMIT 21
SELECT "author_author"."id", "author_author"."name", "author_author"."email", "author_author"."bio" FROM "author_author" WHERE "author_author"."id" = 2 LIMIT 21
SELECT "author_author"."id", "author_author"."name", "author_author"."email", "author_author"."bio" FROM "author_author" WHERE "author_author"."id" = 2 LIMIT 21
```

Now we can use the decorator to measure the queries used when querying using select_related.

```python
@database_debug
def select_related_query():
    blogs = models.Blog.objects.select_related('author').all()
    return [blog.author.name for blog in blogs]

select_related_query()

##################
OUTPUT Result

function_name: select_related_query
query_count: 1
queries:
SELECT "blog_blog"."id", "blog_blog"."title", "blog_blog"."content", "blog_blog"."author_id", "blog_blog"."created_at", "blog_blog"."updated_at", "author_author"."id", "author_author"."name", "author_author"."email", "author_author"."bio" FROM "blog_blog" INNER JOIN "author_author" ON ("blog_blog"."author_id" = "author_author"."id")

```

Now we can use the decorator to measure the queries used when querying using prefetch_related.

```python
@database_debug
def prefetch_related_query():
    blogs = models.Blog.objects.prefetch_related('author').all()
    return [blog.author.name for blog in blogs]

prefetch_related_query()

##################
OUTPUT Result
function_name: prefetch_related_query
query_count: 2
queries:
SELECT "blog_blog"."id", "blog_blog"."title", "blog_blog"."content", "blog_blog"."author_id", "blog_blog"."created_at", "blog_blog"."updated_at" FROM "blog_blog"
SELECT "author_author"."id", "author_author"."name", "author_author"."email", "author_author"."bio" FROM "author_author" WHERE "author_author"."id" IN (1, 2)
```


