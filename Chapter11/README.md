# Chapter 11: Dockerizing Django Application

## Table of contents
* [Technical requirements](#technical-requirements)
* [Using Docker for our Django Application](#using-docker-for-our-django-application)
    * [Creating Dockerfile for Django project](#creating-dockerfile-for-django-project)
    * [Composing services using docker-compose.yaml](#composing-services-using-docker-composeyaml)
    * [Creating a .env file](#creating-a-env-file)
    * [Accessing environment variables in Django](#accessing-environment-variables-in-django)
    * [Starting Django Application using Docker](#starting-django-application-using-docker)


## Technical requirements

## Using Docker for our Django Application

### Creating Dockerfile for Django project

Dockerfile
```Dockerfile
# Pull the official base image 
FROM python:3.11-slim-bullseye 

# Set environment variables 
ENV PYTHONDONTWRITEBYTECODE 1 
ENV PYTHONUNBUFFERED 1 

# Install different Linux packages. 
RUN apt-get update \ 
&& apt-get install gcc postgresql postgresql-contrib libpq-dev python3-dev netcat -y \ 
&& apt-get clean 

# set working directory and install packages using pip. 
WORKDIR /app 
COPY ./requirements ./requirements 
RUN pip install -r requirements/dev-requirements.txt 

# Copy the Application code 
COPY . /app/ 

# Give permission to entrypoint.sh file as executable. 
RUN chmod +x /app/entrypoint.sh 

# run entrypoint.sh 
ENTRYPOINT ["/app/entrypoint.sh"] 
```

entrypoint.sh
```bash
#!/bin/sh 

if [ "$DATABASE" = "postgres" ] 
then 
    echo "Waiting for Postgres..." 

    while ! nc -z $SQL_HOST $SQL_PORT; do 
      sleep 0.1 
    done 

    echo "PostgreSQL started" 
fi 

python manage.py makemigrations 
python manage.py migrate 

exec "$@" 
```

### Composing services using docker-compose.yaml
docker-compose.yaml
```YAML
version: "3.8" 
services: 
  postgresql_db: 
    image: postgres:15-bullseye 
    volumes: 
      - ~/volumes/proj/s/postgres:/var/lib/postgresql/data/ 
    ports: 
      - 5432:5432 
    environment: 
      - POSTGRES_USER=${DB_USER} 
      - POSTGRES_PASSWORD=${DB_PASSWORD} 
      - POSTGRES_DB={PG_DATABASE} 

  redis_db: 
    image: redis:7.2-bullseye 
    container_name: redis_db 
    ports: 
      - 6379:6379 
    command: redis-server --requirepass ${REDIS_PASSWORD} 
    volumes: 
      - $PWD/redis-data:/var/lib/redis 
      - $PWD/redis.conf:/usr/local/etc/redis/redis.conf 

  blog-app: 
    build: ./backend 
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
    command: celery -A backend worker -l info  
    volumes: 
      - ./backend/:/app/ 
    env_file: 
      - ./.env 
    depends_on: 
      - postgresql_db 
      - redis_db 

  celery-beat: 
    build: ./backend 
    command: celery -A backend beat -l info -S redbeat.RedBeatScheduler 
    volumes: 
      - ./backend/:/app/ 
    env_file: 
      - ./.env 
    depends_on: 
      - postgresql_db 
      - redis_db 
```

### Creating a .env file

```bash
DEBUG=True 
DJANGO_ALLOWED_HOSTS=* 
DB_ENGINE=django.db.backends.postgresql 
DB_NAME=django_demo 
DB_USERNAME=root 
DB_PASSWORD=root 
DB_HOSTNAME=postgresql_db 
DB_PORT=5432 
PG_DATABASE=postgres 
REDIS_HOST=redis_db 
REDIS_PORT=6379 
REDIS_PASSWORD=redisPassWord 
```
[Read more](https://docs.docker.com/compose/environment-variables/set-environment-variables/)

### Accessing environment variables in Django

```python
import os 
DEBUG = os.environ.get("DEBUG", False) 
```

### Starting Django Application using Docker

```bash
docker-compose -f docker-compose.yaml up --build 
```
