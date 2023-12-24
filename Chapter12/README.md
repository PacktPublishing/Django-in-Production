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

[“Version Control with Git” by Udacity](https://www.udacity.com/course/version-control-with-git--ud123)  

[“Pro Git” by Scott Chacon and Ben Straub](https://git-scm.com/book/en/v2) 

[“RY’s Git Tutorial” by Ryan Hodson](https://www.amazon.com/Rys-Git-Tutorial-Ryan-Hodson-ebook/dp/B00QFIA5OC) 


## Using GIT efficiently

To use git efficiently, we need to configure git with our name and email address. We can do that by running the following commands in the terminal.

```bash
git config --global user.name "Your Name"
git config --global user.email "you@gmail.com"
```

### Branching strategy for git

Different organizations follow different branching strategies. Some of the most popular branching strategies are listed below.
- [From git official website](https://git-scm.com/book/en/v2/Git-Branching-Branching-Workflows)

- [One of the earliest git workflows by Vincent Driessen is still referred to across organizations. ](https://nvie.com/posts/a-successful-git-branching-model/)

- [GitHub workflow](https://docs.github.com/en/get-started/quickstart/github-flow)
  
- [GitLab workflow](https://docs.gitlab.com/ee/topics/gitlab_flow.html)

### Following good practices while using git commit

No code applicable to this section.

#### Conventional Commits (https://www.conventionalcommits.org/)


```bash
<type>[optional scope]: <description>
[optional body]
[optional footer(s)]
```

#### Use JIRA and GitHub Issues in commit messages

[For more details please visit the official documentation of GitHub on how we can use GitHub Issues efficiently ](https://docs.github.com/en/issues/tracking-your-work-with-issues/about-issues). 
To integrate JIRA or other [project management tools using GitHub visit ](https://github.blog/2019-10-14-introducing-autolink-references/)

- [commitlint](https://github.com/conventional-changelog/commitlint)

- [gitlint](https://github.com/jorisroovers/gitlint)

- [commitizen](https://github.com/commitizen-tools/commitizen)

- [cz-cli](https://github.com/commitizen/cz-cli)

### Tools with git

- [git-sim](https://github.com/initialcommit-com/git-sim)
- Github Desktop
- GitKraken

### Integrating Git Hooks to Django Project

### Using lefthook

[Lefthook](https://github.com/evilmartians/lefthook) is a tool that helps us to manage git hooks efficiently. It is a cross-platform tool that can be used with any programming language. It is written in Golang and is very easy to install and use.

```bash
# For MacOS users
brew install lefthook
# For Linux users
curl -1sLf 'https://dl.cloudsmith.io/public/evilmartians/lefthook/setup.deb.sh' | sudo -E bash
sudo apt install lefthook 

# For Windows users with scoop installed
scoop install lefthook

# For Windows users with winget
winget install evilmartians.lefthook
```

Now let us learn how to integrate lefthook by using a small project example. 

- Create a folder `demo-project` and add a file `demo_script.py` with the following content.

```python
def main():
    print("Hello World")
main()
```
Next initialize the git repository and add the file to the git repository.

```bash
git init
```

Next initiate lefthook in the project folder.

```bash
lefthook install
```
This command would create a `lefthook.yml` file in the project folder. The lefthook file has a bunch of demo commands and scripts that we can use to run different commands. 
We will create a simple lefthook config that can easily be understood. 

Add the following content to the `lefthook.yml` file.
```yaml
pre-commit: 
  commands: 
    demo-echo: 
      run: echo "Just Demo command"
    demo-echo2: 
      run: echo "Just Demo command 2"
```

Now run the following command to see the output.

```bash
> git commit -am "intial Commit"

git commit -am "Init commit"
╭──────────────────────────────────────╮
│ 🥊 lefthook v1.5.5  hook: pre-commit │
╰──────────────────────────────────────╯
┃  demo-echo ❯

Just Demo command

┃  demo-echo2 ❯

Just Demo command 2


  ────────────────────────────────────
summary: (done in 0.03 seconds)
✔️  demo-echo
✔️  demo-echo2

[main 30019a4] Init commit
 2 files changed, 9 insertions(+)
 create mode 100644 demo_script.py

```
Now we have left hook installed and configured in our project. We can add more commands to the `lefthook.yml` file and run them before committing the code.

For more details visit the official documentation of lefthook that explains all the features it provides. [Read More](https://github.com/evilmartians/lefthook/blob/master/docs/usage.md)

### Using git merge vs git rebase

No code applicable to this section.

### Performing code release

No code applicable to this section.

### Performing Hot-Fixing to code

No code applicable to this section.

## Working with GitHub and GitHub actions

### Working with GitHub action for the CI pipeline
The quick start guide of GitHub actions explains how to get started with GitHub actions. We are expecting our readers to be familiar with the basics of GitHub Actions or follow the guide to come up to speed before moving to the next section. 
[Read more](https://docs.github.com/en/actions/quickstart)

### Setting up CI pipeline for Django using GitHub Actions

Github actions work only when the code is pushed to the GitHub repository and the `.github` folder is present in the parent folder. We will create a new GitHub repository and push the code to the repository.

One can either create a new project and add the code to the repository or can copy the folder `Django-in-Project/Chapter12/myblog` from the code repository and push it to a new GitHub repository.

Create a new file `.github/workflows/django-ci.yaml` and add the following content.
```YAML
name: Django CI Test Cases
on: push # Run this Action on every code push made.
env:
  DB_NAME: blog_testdb
  DB_USERNAME: root
  DB_PASSWORD: root
  DB_HOSTNAME: 127.0.0.1
  DB_PORT: 5432
  DB_ENGINE: django.db.backends.postgresql
  REDIS_HOST: 127.0.0.1
  REDIS_PORT: 6379
  REDIS_PASSWORD: redisPassWord
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
      redis:
        image: redis:latest
        ports:
          - 6379:6379
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python 3.11
        uses: actions/setup-python@v3
        with:
          python-version: 3.11
      - name: Install Dependencies
        run: |
          cd backend
          python -m pip install --upgrade pip
          pip install -r requirements/requirements-local.txt
      - name: Run Django migrations
        run: |
          cd backend
          python manage.py migrate
      - name: Running Django Test cases
        run: |
          cd backend
          python manage.py test --no-input
```

Now push the code to the GitHub repository and check the actions tab. You will see the CI pipeline running.

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
