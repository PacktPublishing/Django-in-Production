# Chapter 2 Exploring Django ORM, Models and Migrations

## Table of contents
* [Setting up postgreSQL with Django Project](#setting-up-postgresql-with-django-project)
  * [Configuring Django with PostgreSQL](#configuring-django-with-postgresql)
* [Using Models and Django ORM](#using-models-and-django-orm)
  * [Basic ORM concepts](#basic-orm-concepts)


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



```bash