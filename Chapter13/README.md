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

> [!NOTE]
> Please note this chapter uses AWS and github. AWS and github continuously changes their UI and adds new feature, so it can be possible that the UI might be different from the screenshots in the book. Please use the latest UI and follow the steps mentioned in the book.
> The code examples added in this chapter are tested with MacOS and Linux based systems. If you are using Windows, though the code should work seamlessly for Windows systems but you might need to refer to the official documentation for minor changes needed.

> [!NOTE]
> 
> Join the Discord server "[Django in Production](https://discord.gg/FCrGUfmDyP)" for direct support from the author as you follow the instructions in the book. Feel free to reach out for any help or clarifications needed. https://discord.gg/FCrGUfmDyP.


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

Create a new file with all the env variables in the root of the repository. The file should be named `.env`
```
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

Now run `docker compose up --build` to make sure that the application is running fine.

Let us now start integrating the application with AWS ElasticBeanstalk.

Install the AWS EBCLI using the following command.

```bash
pip install awsebcli
```

Now run the following command to initialize the Elastic Beanstalk environment.

```bash
eb init
```
Follow the steps as mentioned in the wizard. 

Next run the following command to create the environment.

```bash
eb create prod-env
```

Now open the URL in the browser and you should see the application running.

#### Creating RDS Postgres instance and connecting to Django

No code needed for this section.

##### Creating a new RDS environment

No code needed for this section.

##### Connecting RDS to the Django server

No code needed for this section.

##### Configuring Django application with the RDS

Let us now connect RDS to the Beanstalk environment. Follow the steps mentioned in Chapter 13.

Now create a file `.env` in the root of the repository and add the following environment variables.

```bash
DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USERNAME=<RDS USERNAME>
DB_PASSWORD=<RDS PASSWORD>
DB_HOSTNAME=<RDS HOSTNAME>
DB_PORT=<RDS PORT>
REDIS_HOST=redis_db
REDIS_PORT=6379
```

#### Creating ElastiCache Redis instance and connecting to Django

Now create a file `.env` in the root of the repository and add the following environment variables.

```bash
DEBUG=True
DJANGO_ALLOWED_HOSTS=*
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
DB_USERNAME=<RDS USERNAME>
DB_PASSWORD=<RDS PASSWORD>
DB_HOSTNAME=<RDS HOSTNAME>
DB_PORT=<RDS PORT>
REDIS_HOST=<REDIS HOST>
REDIS_PORT=<REDIS PORT>
```

## Deploying Django application using GitHub actions in Elastic Beanstalk

[AWS has official GitHub actions ](https://github.com/aws-actions/configure-aws-credentials) 

Create a new file in the root of the repository named `.github/workflows/deploy-django.yml` and add the following code.
```YAML
name: Github-AWS actions integration
on: [workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.11]
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

      - name: Install aws cli and beanstalk cli
        run: pip install awsebcli awscli

      - name: Get Secret Names by Prefix
        uses: aws-actions/aws-secretsmanager-get-secrets@v1
        with:
          secret-ids: |
            django*    # Retrieves all secrets that start with 'django'

      - name: Save secret manager variables to .env
        run: printenv | grep "^DJANGO" > .env

      - name: git add for .env
        run: git add .

      - name: Run eb init
        run: eb init django-demo-app --region ap-south-1 --platform docker

      - name: Run eb use
        run: eb use prod-env --region ap-south-1

      - name: Run eb deploy
        run: eb deploy --staged
```

Now add the secrets to the repository. Go to the repository settings and click on secrets. Add the following secrets.
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_KEY`

Now we have our GitHub actions ready. Let us push the code to the repository and deploy to production.

----

Elastic beanstalk can also be configured using `.ebextensions` folder. Please check the [official documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/ebextensions.html) for more details.

We have added a sample in `.ebextensions/01_initial_setup.config` file. With the following code.

```
option_settings:
  aws:ec2:instances:
    InstanceTypes: 't3.micro'

container_commands:
    # Demo command to show how to use how to use ebextensions
    01_demo_command:
        command: echo "This is demo command"

```

Here we are setting the instance type to `t3.micro` and running a demo command. You can add more commands to this file. Or you can create a new file and add more commands.

## Following Best Practices with AWS Infrastructure

Please check - [more details](https://aws.amazon.com/architecture/well-architected/)

### Best practices for RDS

### Best practices for ElastiCache

### Best practices for Elastic Beanstalk

### Best practices for IAM and security

## Troubleshooting
