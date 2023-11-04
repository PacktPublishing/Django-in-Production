# Chapter 1: Setting up Django with DRF

## Table of contents
* [Creating a "Hello World" web app with Django and DRF](#creating-a-hello-world-web-app-with-django-and-drf)
  * [Creating a virtual environment](#creating-a-virtual-environment)
  * [Installing Django](#installing-django)


## Creating a "Hello World" web app with Django and DRF

### Creating a virtual environment
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

### Installing Django 
Installing Django using pip in the activated virtual environment.
```bash
pip install Django==4.2
```

### Create a Django project
```bash
mkdir hello_world && cd hello_world
mkdir backend && cd backend
django-admin startproject config .
```
