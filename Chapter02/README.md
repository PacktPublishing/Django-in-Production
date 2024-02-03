# Chapter 2: Exploring Django ORM, Models and Migrations

## Table of contents
* [Technical requirements](#technical-requirements)
* [Setting up PostgreSQL with a Django Project](#setting-up-postgresql-with-a-django-project)
  * [Creating a PostgreSQL server](#creating-a-postgresql-server)
  * [Configuring Django with PostgreSQL](#configuring-django-with-postgresql)
* [Using models and Django ORM](#using-models-and-django-orm)
    * [Adding Django models](#adding-django-models)
    * [Basic ORM concepts](#basic-orm-concepts)
        * [Null versus blank](#null-versus-blank) 
        * [auto_now versus auto_now_add](#auto_now-versus-auto_now_add)
        * [Avoid using raw SQL queries](#avoid-using-raw-sql-queries)
        * [Using query expressions and database functions](#using-query-expressions-and-database-functions)
        * [Use a reverse foreign key lookup](#use-a-reverse-foreign-key-lookup)
    * [How to get raw query from ORM](#how-to-get-raw-query-from-orm)
    * [Normalization using Django ORM](#normalization-using-django-orm)
        * [OneToOneField](#onetoonefield)
        * [The ForeignKey field](#the-foreignkey-field)
        * [ManyToManyField](#manytomanyfield)
    * [Exploring on_delete options](#exploring-on_delete-options)
    * [Using model inheritance](#using-model-inheritance)
        * [Using abstract base classes](#using-abstract-base-classes)
        * [multi-table inheritance](#multi-table-inheritance)
        * [Proxy models](#proxy-models)
* [Understanding the crux of Django Migration](#understanding-the-crux-of-django-migration)
    * [Demythifying Django Migrations commands](#demythifying-django-migrations-commands)
        * [The makemigrations command](#the-makemigrations-command)
        * [The migrate command](#the-migrate-command)
    * [Performing DB migrations like a pro](#performing-db-migrations-like-a-pro)
        * [Perform reverse migrations](#perform-reverse-migrations)
        * [Use Fake migration](#use-fake-migration)
    * [Avoid custom migration for data migrations](#avoid-custom-migration-for-data-migrations)
    * [Create a system check on duplicate migrations](#create-a-system-check-on-duplicate-migrations)
    * [Adding new fields](#adding-new-fields)
* [Exploring Best Practices for working with models and ORM](#exploring-best-practices-for-working-with-models-and-orm)
    * [Use base models](#use-base-models)
    * [Use timezone.now() for any DateTime related data](#use-timezonenow-for-any-datetime-related-data)
    * [How to avoid circular dependency in models](#how-to-avoid-circular-dependency-in-models)
    * [Define __str__ for all models](#define-__str__-for-all-models)
    * [Use custom model methods](#use-custom-model-methods)
    * [Keep the default primary key](#keep-the-default-primary-key)
    * [Use transactions](#use-transactions)
    * [Avoid generic foreign keys](#avoid-generic-foreign-keys)
    * [Use finite state machines (FSMs)](#use-finite-state-machines-fsms)
    * [Break the model into packages](#break-the-model-into-packages)
* [Learning about Performance Optimization](#learning-about-performance-optimization)
  * [Demystifying performance using explain and analyze](#demystifying-performance-using-explain-and-analyze)
  * [Using index](#using-index)
  * [Using Django ORM like a pro](#using-django-orm-like-a-pro)
    * [Exists versus count](#exists-versus-count)
    * [Taking advantage of the lazy loading of QuerySet](#taking-advantage-of-the-lazy-loading-of-queryset)
    * [Using select_related and prefetch_related](#using-select_related-and-prefetch_related)
    * [Avoid bulk_create and bulk_update](#avoid-bulk_create-and-bulk_update)
    * [Using get_or_create and update_or_create](#using-get_or_create-and-update_or_create)
  * [Database Connection configuration](#database-connection-configuration)
    * [Using CONN_MAX_AGE](#using-conn_max_age)
    * [Using connect_timeout](#using-connect_timeout)
* [Exploring Django Async ORM](#exploring-django-async-orm)
* [Summary](#summary)

## Technical requirements

Remote PostgreSQL server - ElephantSQL [website](https://www.elephantsql.com/)

Database management GUI Tool - TablePlus [website](https://tableplus.com/)

If you have any doubts about any of the topics mentioned in this or other chapters, feel free to create GitHub issues that specify all the relevant information (https://github.com/PacktPublishing/Django-in-Production/issues) or join our Django in Production Discord channel and ask for any help. 

> [!NOTE]
> 
> Here is the invite link for the Discord server, where you can reach can post any help and also reachout to me directly: https://discord.gg/FCrGUfmDyP

## Setting up PostgreSQL with a Django Project

Supported databases such as MySQL, MariaDB, and Oracle [More Info](https://docs.djangoproject.com/en/stable/ref/databases/#databases)

### Creating a PostgreSQL server

Follow the steps from the book.

### Configuring Django with PostgreSQL

Install psycopg2-binary using pip in the activated virtual environment.

```bash
pip install psycopg2-binary
```

Replace the default database configuration in the settings.py file with the following:

Your current database configuration should be connecting to SQLite3. And the `settings.py` files should have the `DATABASES` setup config like this -

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

Now, we need to change the database configuration to connect to PostgreSQL. The `settings.py` file be updated with the following `DATABASES` config:

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

## Using models and Django ORM

Django ORM [More Info]( https://docs.djangoproject.com/en/stable/ref/models/querysets/)

### Adding Django models

Create new django apps using the following command:
```bash
python manage.py startapp author
python manage.py startapp blog
```

Add the newly created apps to the `INSTALLED_APPS` list in the `settings.py` file.

```python
CUSTOM_APPS = [
    "author",
    "blog",
]
```

Go the `author/models.py` file and add the `Author` model code as mentioned below-

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return self.name

```

Add the `Blog` model code to the `blog/models.py` file

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

Now create the migration files using the following command:

```bash
python manage.py makemigrations
```

To run the migration, use the following command:
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

#### Null versus blank

```python
from django.db import models

class Author(models.Model):
    ...
    bio = models.TextField(null=True, blank=True)
```

#### auto_now versus auto_now_add

```python
from django.db import models

class Blog(models.Model):
    ...
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ...
```

#### Avoid using raw SQL queries

No code applicable to this section

#### Using query expressions and database functions

For query expressions, [check out](https://docs.djangoproject.com/en/stable/ref/models/expressions/)

For database functions, [check out](https://docs.djangoproject.com/en/stable/ref/models/database-functions/)

#### Use a reverse foreign key lookup

Author and Blog model code as added in the previous section


```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey('author.Author', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Now to work with the model objects let us open Django shell using the following command:

```bash
python manage.py shell
```

Access an author object using via a blog object.
```python
from blog import models as blog_models
author_obj = blog_models.Blog.objects.get(id=1).author
author_obj
```

Fetch the blog information from an author object, we can use a reverse foreign key lookup
```python
from author import models as author_models
author = author_models.Author.objects.get(email='john@gmail.com')
all_blogs_by_an_author = author.blog_set.all()
print(all_blogs_by_an_author)

selected_blog = author.blog_set.filter(title='Python is cool')
print(selected_blog)
```

### How to get raw query from ORM

Retrieving Queries for ORM using `.query`

```python
from author import models

all_authors = models.Author.objects.filter(email__endswith='@gmail.com').values_list('name').query

print(all_authors)
```

Retrieving Queries for ConnectionProxy

```python
from django.db import connection
from author import models

author_count = models.Author.objects.filter(email='a').count()
connection.queries[-1]
```

### Normalization using Django ORM

No code applicable to this section

#### OneToOneField

OneToOneField is like ForeignKey, with an additional constraint of unique=True on ForeignKey

```python
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='author_blogs', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.OneToOneField('CoverImage', related_name='blog_cover_image', on_delete=models.PROTECT)

class CoverImage(models.Model):
    image_link = models.URLField()
```

#### The ForeignKey field

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='author_blogs', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```
#### ManyToManyField

Create a new model `Tag` and add the following code to the `blog/models.py` file

```python
class Tag(models.Model):
    name = models.CharField(max_length=100)
    
class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='author_blogs', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tag, related_name='blog_tags')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

Customizing ManyToManyField [for more info](https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ManyToManyField.through)

### Exploring on_delete options

No code applicable to this section

#### Using model inheritance

No code applicable to this section

##### Using abstract base classes

```python
class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()
```

##### multi-table inheritance

No code applicable to this section

##### Proxy models

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

class BlogAuthor(Author):
    class Meta:
        proxy = True
    
    def perform_something(self):
        pass
```

## Understanding the crux of Django Migration

No code applicable to this section

### Demythifying Django Migrations commands

No code applicable to this section

#### The makemigrations command

```bash
python manage.py startapp author
python manage.py startapp blog
```

Note: After running above command at this point, this will create 0002 migrations files in migrations folder of author and blog app respectively, this happens due to examples in the book

#### The migrate command

No code applicable to this section

### Performing DB migrations like a pro

No code applicable to this section

#### Perform reverse migrations

```shell
python manage.py migrate blog 0001
```

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

Now run the following commands:
```bash
python manage.py makemigrations
python manage.py migrate author 0002 --fake  # note: always check for migration file no created by previous step
```

We have now faked the migration. Now, if we run the migrate command again, it will not apply the migration.

```bash
python manage.py migrate
```

Now to revert the fake migrations 

```bash
python manage.py migrate author 0001 --fake
```
#### Avoid custom migration for data migrations

No code applicable to this section

#### Create a system check on duplicate migrations

No code applicable to this section

#### Adding new fields

No code applicable to this section

## Exploring Best Practices for working with models and ORM

No code applicable to this section

### Use base models

```python
from django.db import models

class TimeStampedBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class DemoModel(TimeStampedBaseModel):
    name = models.CharField(max_length=100)
```

### Use timezone.now() for any DateTime related data

Django `settings.py` have a `TIME_ZONE` config that we need to set.  [Learn more](https://docs.djangoproject.com/en/5.0/topics/i18n/timezones/)

### How to avoid circular dependency in models

No code applicable to this section

### Define __str__ for all models

```python
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name}-{self.id}'

```

### Use custom model methods

Take the example of the `Author` model, we can add a custom method to get the author's full name and a short bio.
```python
class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    def get_author_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_bio(self):
        return f'{self.bio[:200]}...'
```
### Keep the default primary key

No code applicable to this section

### Use transactions

```python
from django.db import transaction
def viewfunc(request):
    # This code executes in autocommit mode (Django's default).
    # do_db_stuff()
    with transaction.atomic():
        # This code executes inside a transaction.
        pass
        # do_more_db_stuff()
        # do_one_more_db_stuff()
```

### Avoid generic foreign keys

No code applicable to this section

### Use finite state machines (FSMs)

No code applicable to this section

### Break the model into packages

No code applicable to this section

## Learning about Performance Optimization

No code applicable to this section

### Demystifying performance using explain and analyze

read the explain and analyze [more info](https://www.postgresql.org/docs/current/sql-explain.html)

### Using index

```python
class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['name']),
        ]
```

### Using Django ORM like a pro

No code applicable to this section

#### Exists versus count

No code applicable to this section

#### Taking advantage of the lazy loading of QuerySet

No code applicable to this section

#### Using select_related and prefetch_related

To understand the advantage of using select_related and prefetch_related, we need to understand the concept of database joins. And also how Django ORM works using the hood when we have multiple queries.

First we need to create a decorator that we can use to measure the queries used when querying.

```python
from django.db import connection
from django.db import reset_queries

def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func(*args, **kwargs)
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
    return [blog.author.name for blog in blogs]

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

#### Avoid bulk_create and bulk_update

learn more about bulk_create, [go to](https://docs.djangoproject.com/en/stable/ref/models/querysets/#bulk-create)

#### Using get_or_create and update_or_create

bulk_update, [go to](https://docs.djangoproject.com/en/stable/ref/models/querysets/#get-or-create)

### Database Connection configuration

No code applicable to this section

#### Using CONN_MAX_AGE

Django for persistent connections, [go to](https://docs.djangoproject.com/en/stable/ref/databases/#persistent-connections)

#### Using connect_timeout

```python
from django.db.backends.signals import connection_created
from django.dispatch import receiver

@receiver(connection_created)
def setup_query_timeout(connection, **kwargs):
    # Set Timeout for every statement as 60 seconds.
    with connection.cursor() as cursor:
        cursor.execute("set statement_timeout to 60000;")
```

## Exploring Django Async ORM

Python natively supports async-await: [more info](https://docs.python.org/3/library/asyncio-task.html)