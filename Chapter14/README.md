# Chapter 14: Monitoring Django Application

## Table of contents
* [Technical requirements](#technical-requirements)
* [Integrating Error Tracking Tools](#integrating-error-tracking-tools)
    * [Integrating Rollbar into Django Project](#integrating-rollbar-into-django-project)
    * [Integrating Rollbar with Slack](#integrating-rollbar-with-slack)
    * [Best practices while working with Error monitoring tools](#best-practices-while-working-with-error-monitoring-tools)
* [Integrating uptime monitoring](#integrating-uptime-monitoring)
    * [Finding the health check endpoint](#finding-the-health-check-endpoint)
    * [Using BetterStack for uptime monitoring](#using-betterstack-for-uptime-monitoring)
* [Integrating APM tools](#integrating-apm-tools)
    * [Integrating New Relic to Django Project](#integrating-new-relic-to-django-project)
    * [Exploring New Relic Dashboard](#exploring-new-relic-dashboard)
    * [Creating New Relic Alert conditions](#creating-new-relic-alert-conditions)
    * [Monitoring AWS EC2 instances with New Relic](#monitoring-aws-ec2-instances-with-new-relic)
    * [Sending logs from Django to New Relic](#sending-logs-from-django-to-new-relic)
    * [Working with Metrics and Events using NRQL](#working-with-metrics-and-events-using-nrql)
* [Integrating messaging tools Using Slack message actions](#integrating-messaging-tools-using-slack-message-actions)
* [Handling production incidents betters](#handling-production-incidents-betters)
* [Learning Blameless RCA for incidents](#learning-blameless-rca-for-incidents)


## Technical requirements

No code applicable in this section.

## Integrating Error Tracking Tools

Here are few error tracking tools:
- [Rollbar](https://rollbar.com/)
- [Sentry](https://sentry.io/)
- [Bugsnag](https://www.bugsnag.com/)
- [Airbrake](https://airbrake.io/)

### Integrating Rollbar into Django Project

To integrate rollbar into Django project, we need to install rollbar package using pip.
```bash
pip install rollbar
```

Next we need to update `settings.py` file to add rollbar middleware and configuration.
```python
MIDDLEWARE = [ 
# OTHER MIDDLEWARES 
  'rollbar.contrib.django.middleware.RollbarNotifierMiddleware', 
] 
```

Next we need to add rollbar configuration to `settings.py` file.
```python
ROLLBAR = { 
  'access_token': '<token>', 
  'environment': 'dev' if DEBUG else 'prod', 
  'root': BASE_DIR 
} 
```

We have successfully integrated rollbar into Django project. Now we need to test it.
Add the following code to `config/urls.py` file.

```python
from django.http import HttpResponse
def rollbar_test_view(request):
    a = None
    a.hello() # This would raise an exception
    return HttpResponse("Hello World!")

urlpatterns = [
    # ...
    path('rollbar-test/', rollbar_test_view),
]

```
Now when we visit the url `http://127.0.0.1:8000/rollbar-test/`, we would see the error message in rollbar.


### Integrating Rollbar with Slack
Official documentation: [Rollbar Slack Integration](https://docs.rollbar.com/docs/slack)

### Best practices while working with Error monitoring tools

[Sentry](https://sentry.io/) is an open-source alternative

## Integrating uptime monitoring

### Adding health check endpoint

Integrate [Django Health Check ](https://github.com/revsys/django-health-check) to our Django project.

```bash
pip install django-health-check
```

Add `health_check` to Django `INSTALLED_APPS` in `settings.py` file: 

```python
INSTALLED_APPS = [ 
    # …  
    'health_check', 
    'health_check.db',         # Checks database connection 
    'health_check.cache',      # Checks cache backend 
]
```

Now update the `urls.py` to add health check endpoint.
```python
urlpatterns = [ 
    # ... 
    path(r'^ht/', include('health_check.urls')), 
] 
```

Open the url `http://127.0.0.1:8000/ht/` on your browser to see the health check.

### Using BetterStack for uptime monitoring

BetterStack is an uptime monitoring tool. The integration of [BetterStack](https://betterstack.com/) to our django project is easy and can be done following the official documentation.

## Integrating APM tools

There are multiple Application Performance Monitoring(APM) tools available. Some of them are: 
- [New Relic](https://www.newrelic.com/) 
- [AppDynamics](https://www.appdynamics.com/)
- [Datadog](https://www.datadoghq.com/)
- [Dynatrace](https://www.dynatrace.com/)
- [Instana](https://www.instana.com/)

In this book we shall focus on New Relic. NewRelic has an amazing official guide that can be used to learn about the different new relic features. Check [New Relic University](https://learn.newrelic.com/) for more details

### Integrating New Relic to Django Project

To integrate New Relic to Django project, we need to install newrelic package using pip.
```bash
pip install newrelic
```

Next create a new data source in NewRelic Dashboard. Download the `newrelic.ini` file and place it in the root directory of the project, same folder as `manage.py` file.

Validate the newrelic configuration using the following command:
```bash
newrelic-admin validate-config newrelic.ini
```

After the configuration is validated, we can plugin the newrelic agent to our Django project using the following command:
```bash
newrelic-admin run-program python manage.py runserver
```

Now we can open the New Relic dashboard to see the data.

To integrate newrelic to production server, we need to install newrelic package using pip. Add the `newrelic` package to `requirements-base.txt` file.

Update the docker file to run the newrelic agent.
```dockerfile
services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile.prod
    command: newrelic-admin run-program gunicorn backend.prod_wsgi:application --workers 4 --bind 0.0.0.0:8000 --max-requests=512 --max-requests-jitter=64 --reload
    ....
```
We have successfully integrated newrelic to our Django project.


### Exploring New Relic Dashboard

No code applicable in this section.

### Creating New Relic Alert conditions

No code applicable in this section.

### Monitoring AWS EC2 instances with New Relic

[Read more](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/config-management-tools/configure-infrastructure-agent-aws-elastic-beanstalk/)

### Sending logs from Django to New Relic

Now we would tell the new relic infrastructure agent to watch the file content of the `logs/django_logs.log` and send the logs to New Relic.

We have learned about logging in [Chapter06](../Chapter06/README.md). We would use the same logging configuration to send logs to New Relic.
```python
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {"verbose": {"format": "%(asctime)s %(process)d %(thread)d %(message)s"}},
    "loggers": {
        "django_default": {
            "handlers": ["django_file"],
            "level": "INFO",
            "propogate": True,
        },
    },
    "handlers": {
        "django_file": {
            "class": "common.custom_log_handlers.MakeRotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs/django_logs.log"),
            "maxBytes": 1024 * 1024 * 10,  # 10MB
            "backupCount": 10,
            "formatter": "verbose"
        },
    },
}
```

Now Create a `logging.yaml` config file that would be used by newrelic infrastructure agent to identify logs and then forward the logs to newrelic.
```yaml
logs:
  - name: "django_log"
    file: /<log file path>/*.log #update the log file path
  - name: "nginx_log"
    file: /<nginx log file path/*.log
  - name: "etc_log" # any other log we want to send
    file: /path/*.log
```

Once the `logging.yaml` file is created, would use ebextensions to setup the config. Create a file `.ebextensions/02_newrelic_logging.config` and add the following content to it.
```yaml
container_commands:
  01_copy_logging_config:
    command: "cp .ebextensions/logging.yaml /etc/newrelic-infra/logging.d/"
```

Now when we would perform `eb deploy`, the newrelic infrastructure agent would start sending logs to newrelic.

### Working with Metrics and Events using NRQL

- https://docs.newrelic.com/docs/query-your-data/nrql-new-relic-query-language/get-started/introduction-nrql-new-relics-query-language/

## Integrating messaging tools Using Slack message actions

- https://slack.com/intl/en-in/resources/using-slack/speed-up-software-development-with-slack
- https://slack.com/intl/en-in/resources/why-use-slack/the-value-of-slack-for-software-developers
- https://slack.com/intl/en-in/resources/why-use-slack/software-development-teams-and-slack
- https://slack.com/intl/en-in/resources/why-use-slack/how-it-works-slack-for-software-development
- https://slack.com/intl/en-in/resources/why-use-slack/how-slacks-own-developers-use-slack

## Handling production incidents betters

Different tools that can be used to handle production incidents:
- [PagerDuty](https://www.pagerduty.com/)
- [OpsGenie](https://www.atlassian.com/software/opsgenie)
- [VictorOps](https://victorops.com/)
- [Squadcast](https://www.squadcast.com/)

## Learning Blameless RCA for incidents

Blameless RCA is a process that helps us to identify the root cause of an incident without blaming anyone. It is a process that helps us to learn from the incident and improve the system. Here are a few resources that can help us to learn more about Blameless RCA:
- https://www.atlassian.com/incident-management/kpis/blameless-rca
- https://www.atlassian.com/incident-management/kpis/blameless-rca/what-is-blameless-rca
- https://about.gitlab.com/handbook/customer-success/professional-services-engineering/workflows/internal/root-cause-analysis.html
- https://postmortems.pagerduty.com/culture/blameless/


