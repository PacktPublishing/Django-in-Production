# Chapter 13: Deploying Django in AWS

## Table of contents
* [Technical requirements](#technical-requirements)
* [Learning the Basics of AWS](#learning-the-basics-of-aws)
    * [Creating an account in AWS](#creating-an-account-in-aws)
    * [Identity and Access Management](#identity-and-access-management)
    * [EC2](#ec2)
    * [Elastic Load Balancer](#elastic-load-balancer)
    * [Elastic Beanstalk](#elastic-beanstalk)
    * [RDS for Postgres](#rds-for-postgres)
    * [Elasticache for Redis](#elasticache-for-redis)
    * [Security Groups and Network components](#security-groups-and-network-components)
    * [AWS Secrets Manager](#aws-secrets-manager)
    * [Route 53](#route-53)
    * [AWS Billing Console](#aws-billing-console)
    * [Cloudwatch](#cloudwatch)
* [Integrating AWS Elastic Beanstalk to deploy Django](#integrating-aws-elastic-beanstalk-to-deploy-django)
    * [Integrating Beanstalk with basic Django app](#integrating-beanstalk-with-basic-django-app)
      * [Creating RDS Postgres instance and connecting to Django](#creating-rds-postgres-instance-and-connecting-to-django)
          * [Creating a new RDS environment](#creating-a-new-rds-environment)
          * [Connecting RDS to the Django server ](#connecting-rds-to-the-django-server)
          * [Configuring Django application with the RDS](#configuring-django-application-with-the-rds)
      * [Creating ElastiCache Redis instance and connecting to Django](#creating-elasticache-redis-instance-and-connecting-to-django)
    * [Deploying Django application using GitHub actions in Elastic Beanstalk](#deploying-django-application-using-github-actions-in-elastic-beanstalk)
* [Following Best Practices with AWS Infrastructure](#following-best-practices-with-aws-infrastructure)
    * [Best practices for RDS](#best-practices-for-rds)
    * [Best practices for ElastiCache](#best-practices-for-elasticache)
    * [Best practices for Elastic Beanstalk](#best-practices-for-elastic-beanstalk)
    * [Best practices for IAM and security](#best-practices-for-iam-and-security)
* [Troubleshooting](#troubleshooting)


## Technical requirements

## Learning the Basics of AWS
[AWS Account](https://aws.amazon.com)

### Creating an account in AWS

Go to [AWS](https://aws.amazon.com) and create an account. You will need a credit card to create an account.

### Identity and Access Management

No code needed for this section. Just learn about IAM and how to create users, groups, and policies.

### EC2

No code needed for this section.

### Elastic Load Balancer

No code needed for this section.

### Elastic Beanstalk

No code needed for this section.

### RDS for Postgres

No code needed for this section.

### Elasticache for Redis

No code needed for this section.

### Security Groups and Network components

No code needed for this section.

### AWS Secrets Manager

No code needed for this section.

### Route 53

No code needed for this section.

### AWS Billing Console

No code needed for this section.

### Cloudwatch

No code needed for this section.

## Integrating AWS Elastic Beanstalk to deploy Django

### Integrating Beanstalk with basic Django app

> [!NOTE]
> 
> Our current repository is a repository that we have been working on for the last 12 chapters, where each chapter is segregated into folders. Unfortunately just like github actions we cannot deploy a repository with multiple project folders. So we will create a new repository with just the Django application.
> The simplest way to do this is to create a new repository and copy the Django application folder into the new repository. Please copy the myblog folder into a new repository. 



#### Creating RDS Postgres instance and connecting to Django

##### Creating a new RDS environment

##### Connecting RDS to the Django server

##### Configuring Django application with the RDS

In settings.py

```python
DATABASES = { 
    "default": { 
        "ENGINE": 'django.db.backends.postgresql', 
        "NAME": 'postgres', 
        "USER": 'django_db_user', 
        "PASSWORD": 'abc^A12a*12', 
        "HOST": 'django-demo.cz2r2xzvhh2n.ap-south-1.rds.amazonaws.com', 
        "PORT": '5432', 
    } 
} 
```

#### Creating ElastiCache Redis instance and connecting to Django

In settings.py

```python
CACHES = { 
    "default": { 
        "BACKEND": "django.core.cache.backends.redis.RedisCache", 
        "LOCATION": "redis://django-demo-cache.dysbo0.ng.0001.aps1.cache.amazonaws.com:6379", 
    } 
} 
```

## Deploying Django application using GitHub actions in Elastic Beanstalk

[AWS has official GitHub actions ](https://github.com/aws-actions/configure-aws-credentials) 

```YAML
name: Test Github-AWS actions integration 

on: [workflow_dispatch] 

jobs: 
  build: 
    runs-on: ubuntu-latest 
    strategy: 
      matrix: 
        python-version: [3.8] 
    steps: 

      - uses: actions/checkout@v1 
      - name: Configure AWS Credentials 
        uses: aws-actions/configure-aws-credentials@v4 
        with: 
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }} 
          aws-secret-access-key: ${{ secrets.AWS_SECRET_KEY }} 
          aws-region: us-east-2 

      - name: get caller identity 
        run: aws sts get-caller-identity 
```

## Following Best Practices with AWS Infrastructure

Please check - [more details](https://aws.amazon.com/architecture/well-architected/)

### Best practices for RDS

### Best practices for ElastiCache

### Best practices for Elastic Beanstalk

### Best practices for IAM and security

## Troubleshooting

