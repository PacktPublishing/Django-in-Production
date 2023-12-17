# Chapter 12: Working with Git and CI pipeline using Django

## Table of contents
* [Technical requirements](#technical-requirements)
* [Using GIT efficiently](#using-git-efficiently)
    * [Branching strategy for git](#branching-strategy-for-git)
    * [Following good practices while using git commit](#following-good-practices-while-using-git-commit)
        * [Conventional Commits (https://www.conventionalcommits.org/)](#conventional-commits-https-www-conventionalcommits-org)
        * [Use JIRA and GitHub Issues in commit messages](#use-jira-and-github-issues-in-commit-messages)
    * [Tools with git](#tools-with-git)
    * [Integrating Git Hooks to Django Project](#integrating-git-hooks-to-django-project)
    * [Using lefthook](#using-lefthook)
    * [Using git merge vs git rebase](#using-git-merge-vs-git-rebase)
    * [Performing code release](#performing-code-release)
    * [Performing Hot-Fixing to code](#performing-hot-fixing-to-code)
* [Working with GitHub and GitHub actions](#working-with-github-and-github-actions)
    * [Working with GitHub action for the CI pipeline](#working-with-github-action-for-the-ci-pipeline)
    * [Setting up CI pipeline for Django using GitHub Actions](#setting-up-ci-pipeline-for-django-using-github-actions)
    * [Recommended GitHub Actions resources](#recommended-github-actions-resources)
* [Setting up Code Review Guidelines](#setting-up-code-review-guidelines)
    * [Context and Description](#context-and-description)
    * [Short Code Changes to Review](#short-code-changes-to-review)
    * [Review when the Code is Ready](#review-when-the-code-is-ready)
    * [Good Code Reviewer](#good-code-reviewer)


## Technical requirements

[“Version Control with Git” by Udacity –](https://www.udacity.com/course/version-control-with-git--ud123)  

[“Pro Git” by Scott Chacon and Ben Straub – ](https://git-scm.com/book/en/v2) 

[“RY’s Git Tutorial” by Ryan Hodson – ](https://www.amazon.com/Rys-Git-Tutorial-Ryan-Hodson-ebook/dp/B00QFIA5OC) 


## Using GIT efficiently

### Branching strategy for git

[From git official website - ](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

[One of the earliest git workflows by Vincent Driessen is still referred to across organizations. ](https://nvie.com/posts/a-successful-git-branching-model/)

[GitHub workflow - ](https://docs.github.com/en/get-started/quickstart/github-flow)

[GitLab workflow - ](https://docs.gitlab.com/ee/topics/gitlab_flow.html)

### Following good practices while using git commit

#### Conventional Commits (https://www.conventionalcommits.org/)

#### Use JIRA and GitHub Issues in commit messages

[For more details please visit the official documentation of GitHub on how we can use GitHub Issues efficiently ](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues). 
To integrate JIRA or other [project management tools using GitHub visit ](https://github.blog/2019-10-14-introducing-autolink-references/)

[commitlint – ](https://github.com/conventional-changelog/commitlint)

[gitlint – ](https://github.com/jorisroovers/gitlint)

[commitizen - ](https://github.com/commitizen-tools/commitizen)

[cz-cli - ](https://github.com/commitizen/cz-cli)

### Tools with git

### Integrating Git Hooks to Django Project

### Using lefthook

lefthook.yml
```YAML
pre-commit: 
  commands: 
    frontend-linter: 
      run: yarn eslint {staged_files} 
    python-linter: 
      run: black {source_file_or_directory} 
    demo: 
      run: echo "Just Demo script"   
```

[For more details visit the official documentation of lefthook that explains all the features it provides](https://github.com/evilmartians/lefthook/blob/master/docs/usage.md)

### Using git merge vs git rebase

### Performing code release

### Performing Hot-Fixing to code

## Working with GitHub and GitHub actions

### Working with GitHub action for the CI pipeline
The quick start guide of GitHub actions explains how to get started with GitHub actions. We are expecting our readers to be familiar with the basics of GitHub Actions or follow the guide to come up to speed before moving to the next section. 
[Read more](https://docs.github.com/en/actions/quickstart)

### Setting up CI pipeline for Django using GitHub Actions

```YAML
name: Django CI Test Cases 
on: push # Run this Action on every code push made. 
env: 
  RDS_DB_NAME: blog_testdb 
  RDS_USERNAME: root 
  RDS_PASSWORD: root 
  RDS_HOSTNAME: 127.0.0.1 
  RDS_PORT: 5432 
  SQL_ENGINE: django.db.backends.postgresql     

jobs: 
  # Label of the container job 
  container-job: 
    runs-on: ubuntu-latest 
    services: 
      postgres: 
        image: postgres:latest 
        env: 
          POSTGRES_USER: root 
          POSTGRES_PASSWORD: root 
          POSTGRES_DB: blog_testdb 
        ports: 
          - 5432:5432 
        # Set health checks to wait until Postgres has started 
        options: >- 
          --health-cmd pg_isready 
          --health-interval 10s 
          --health-timeout 5s 
          --health-retries 5 

    steps: 
     - uses: actions/checkout@v3 
     - name: Set up Python 3.9 
       uses: actions/setup-python@v3 
       with: 
         python-version: 3.9 
     - name: Install Dependencies 
       run: pip install -r requirements/ci-requirements-base.txt 

     - name: Run Django migrations 
       run: python manage.py migrate 

     - name: Running Django Test cases 
       run: python manage.py test --no-input 
```

GitHub actions, check the official documentation for [more details](https://docs.github.com/en/actions/using-workflows/events-that-trigger-workflows)

### Recommended GitHub Actions resources

[Send slack message whenever there is some action performed on the code repository using the pipeline, like deployment, etc. ](https://github.com/marketplace/actions/slack-send)

[Perform linting using GitHub actions ](https://github.com/marketplace/actions/super-linter)

[Check for any secret key accidentally committed in the code repository ](https://github.com/marketplace/actions/trufflehog-oss)

## Setting up Code Review Guidelines

### Context and Description

### Short Code Changes to Review

### Review when the Code is Ready

### Good Code Reviewer
