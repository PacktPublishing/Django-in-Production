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

Now run the following command to start the development server:
```bash
python manage.py runserver
```

Open your browser and go to the following URL: http://127.0.0.1:8000/ or http://localhost:8000/ to see the Django welcome page.

### Creating our first app in Django

### Linking app views using urls.py


### Integration DRF

In order to install Django Rest Framework, we need to install it using pip in the activated virtual environment.

```bash
pip install djangorestframework
```

## Creating RESTful API endpoints with DRF

### Best practices for defining RESTful APIs

### Best practices to create a REST API with DRF

#### Using API versioning

##### Using a custom version class with DRF

#### Avoid Router

### Working with views using DRF

#### Functional views

#### Class-based views

##### APIView

##### Generic Views

## Introducing API development tools