# Chapter 11: Dockerizing Django Application

## Table of contents
* [Technical requirements](#technical-requirements)
* [Learning the basics of Docker](#learning-the-basics-of-docker)
  * [Installing Docker](#installing-docker)
  * [Testing Docker in local](#testing-docker-in-local)
  * [Important Commands for Docker](#important-commands-for-docker)
* [Working with requirements.txt file](#working-with-requirementstxt-file)
* [Creating Dockerfile for Django project](#creating-dockerfile-for-django-project)
* [Composing services using docker-compose.yaml](#composing-services-using-docker-composeyaml)
  * [Creating a .env file](#creating-a-env-file)
  * [Accessing environment variables in Django](#accessing-environment-variables-in-django)
  * [Starting Django Application using Docker](#starting-django-application-using-docker)


## Technical requirements

No code applicable to this section.

## Learning the basics of Docker

### Installing Docker

- For MacOS users - Please follow the steps mentioned in https://docs.docker.com/desktop/install/mac-install/
- For Windows users – Please follow the steps mentioned in https://docs.docker.com/desktop/install/windows-install/
- For Linux users – Please follow the steps mentioned in https://docs.docker.com/desktop/install/linux-install/

Once docker is installed in your system, you can verify the installation by running the following command in your terminal.

```bash
docker version 
```

### Testing Docker in local

To test the docker installation, you can run the following command in your terminal.
```bash
docker pull hello-world  && docker run hello-world
```


### Important Commands for Docker

Learn more about the docker command https://docs.docker.com/engine/reference/run/

## Working with requirements.txt file

Break the `requirements.txt` file into multiple files

- `requirements/requirements-base.txt` - This file will contain all the packages that are required for the project to run in any environment.
- `requirements/requirements-local.txt` - This file will contain all the packages that are required for the project to run in development environment.

Create a new file `backend/requirements/requirements-base.txt` and add the following content.

```txt
Django==5.0
redis==5.0.1
django-cacheops==7.0.2
celery==5.3.6
psycopg2-binary==2.9.9
djangorestframework==3.14.0
celery-redbeat==2.1.1
```

Create a new file `backend/requirements/requirements-local.txt` and add the following content.

```txt
-r requirements-base.txt
factory_boy==3.3.0
django-debug-toolbar==3.2.2
```

## Creating Dockerfile for Django project

Create a new file `backend/Dockerfile` and add the following content.
```Dockerfile
# Pull the official base image
FROM python:3.11
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Install different Linux packages.
RUN apt-get update \
&& apt-get install gcc postgresql postgresql-contrib libpq-dev python3-dev netcat-traditional -y \
&& apt-get clean
# set working directory and install packages using pip.
WORKDIR /app
COPY ./requirements ./requirements
RUN pip install -r requirements/requirements-local.txt

# Copy the Application code
COPY . /app/


COPY ./entrypoint.sh /app/entrypoint.sh

# Give permission to entrypoint.sh file as executable.
RUN chmod +x /app/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
```

Create a new file `backend/entrypoint.sh` and add the following content.
```bash
#!/bin/sh

if [ "$DB_HOSTNAME" = "postgresql_db" ]; then
    echo "Waiting for Postgres..."
    while ! nc -z $DB_HOSTNAME $DB_PORT; do
      sleep .1
      echo "Waiting for Postgres...1"
    done
    echo "PostgreSQL started"
fi

python manage.py migrate
exec "$@"
```

Now run the following command to build the docker image.
```bash
docker build -f ./Dockerfile -t django-in-production .
```

Now run the following command to run the docker image.
```bash
docker run -p 0.0.0.0:8000:8000 django-in-production python manage.py runserver 0.0.0.0:8000
```

We have our django application running in docker container and accessible at [http://0.0.0.0:8000/admin](http://0.0.0.0:8000/admin)

In our docker example we are connected to the remote database of ElephantSQL. Now we need to connect to the local database. For that we need to create a postgresql database in our local system.

### Composing services using docker-compose.yaml

Now create `myblog/docker-compose.yaml` file in the root directory of the project and add the following content.
```YAML
version: "3.8"
services:
  postgresql_db:
    image: postgres:16.1
    volumes:
      - ~/volumes/proj/dip/postgres/:/var/lib/postgresql/data/
    ports:
      - 5432:5432
    env_file:
      - ./.env
    environment:
      - POSTGRES_USER=${DB_USERNAME}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
      - POSTGRES_DB=${DB_NAME}
  redis_db:
    image: redis:7.2
    container_name: redis_db
    ports:
      - 6379:6379
    command: redis-server --requirepass ${REDIS_PASSWORD}
    env_file:
      - ./.env
    volumes:
      - $PWD/redis-data:/var/lib/redis
      - $PWD/redis.conf:/usr/local/etc/redis/redis.conf
  blog_app:
    build:
     context: ./backend
     dockerfile: Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ./backend/:/app/
    ports:
      - 8000:8000
    env_file:
      - ./.env
    depends_on:
      - postgresql_db
      - redis_db

  celery:
    build: ./backend
    command: celery --app=config worker -l info
    volumes:
      - ./backend/:/app/
    env_file:
      - ./.env
    depends_on:
      - postgresql_db
      - redis_db
  celery_beat:
    build: ./backend
    command: celery --app=config beat -l info -S redbeat.RedBeatScheduler
    volumes:
      - ./backend/:/app/
    env_file:
      - ./.env
    depends_on:
      - postgresql_db
      - redis_db
```

We need to also give permission to `entrypoint.sh` file as executable.
```bash
chmod +x ./backend/entrypoint.sh
```

Now before running the docker-compose command, we need to create a `.env` file in the root directory of the project and add the following content.

### Creating a .env file

create a `myblog/.env` file in the root directory of the project and add the following content.
```bash
DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=django_in_production
DB_USERNAME=root
DB_PASSWORD=root
DB_HOSTNAME=postgresql_db
DB_PORT=5432
REDIS_HOST=redis_db
REDIS_PORT=6379
REDIS_PASSWORD=redisPassWord
```
[Read more](https://docs.docker.com/compose/environment-variables/set-environment-variables/)

### Accessing environment variables in Django

Here is an example of accessing environment variables in Django.
```python
import os 
DEBUG = os.environ.get("DEBUG", False) 
```

Now we need to update our `settings.py` file to use the environment variables.

For example in `settings.py` file, we need to update the `DATABASES` variable as follows.
```python
import os

DATABASES = {
    'default': {
        'ENGINE': os.environ.get('DB_ENGINE'),
        'HOST': os.environ.get('DB_HOSTNAME'),
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USERNAME'),
        'PORT': os.environ.get('DB_PORT'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'TEST': {
            'NAME': 'mytestdatabase',
        }
    }
}
```


### Starting Django Application using Docker

Now run the following command to start the django application using docker-compose.
```bash
docker-compose -f docker-compose.yaml up --build 
```

Now we have our django application running in docker container and accessible at [http://0.0.0.0:8000/admin](http://0.0.0.0:8000/admin) 

We can verify all the containers running using the following command.
```bash
docker ps
```
