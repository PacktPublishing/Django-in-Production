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

## Integrating Error Tracking Tools

[Rollbar](https://rollbar.com/)

In settings.py
```python
MIDDLEWARE = [ 
# OTHER MIDDLEWARES 'rollbar.contrib.django.middleware.RollbarNotifierMiddleware', 
] 
```
```python
ROLLBAR = { 
  'access_token': '<token>', 
  'environment': 'dev' if DEBUG else 'prod', 
  'root': BASE_DIR 
} 
```

Django view
```python
def index(request): 
    a = None 
    a.hello() # This would raise an exception 
    return HttpResponse("Hello World!")
```

### Integrating Rollbar into Django Project


### Integrating Rollbar with Slack

### Best practices while working with Error monitoring tools

[Sentry](https://sentry.io/) is an open-source alternative

## Integrating uptime monitoring

### Finding the health check endpoint

[Django Health Check ](https://github.com/revsys/django-health-check)

health_check to Django INSTALLED_APPS in settings.py file: 

```python
INSTALLED_APPS = [ 
    # …  
    'health_check', 
    'health_check.db',         # Checks database connection 
    'health_check.cache',      # Checks cache backend 
]
```

urls.py
```python
urlpatterns = [ 
    # ... 
    url(r'^ht/', include('health_check.urls')), 
] 
```

### Using BetterStack for uptime monitoring

[BetterStack](https://betterstack.com/)

## Integrating APM tools

[New Relic](https://www.newrelic.com/)

[New Relic University](https://learn.newrelic.com/)

### Integrating New Relic to Django Project

### Exploring New Relic Dashboard

### Creating New Relic Alert conditions

### Monitoring AWS EC2 instances with New Relic

[Read more](https://docs.newrelic.com/docs/infrastructure/install-infrastructure-agent/config-management-tools/configure-infrastructure-agent-aws-elastic-beanstalk/)

### Sending logs from Django to New Relic

Now we would tell the new relic infrastructure agent to watch the file content of the path/to/django_logs.log and send the logs to New Relic. 
```python
LOGGING = { 
 "version": 1, 
 "disable_existing_loggers": False, 
 "formatters": {"verbose": {"format": "%(asctime)s %(process)d %(thread)d %(message)s"}}, 
 "loggers": { 
    "django_default": { 
        "handlers": ["django_file"], 
        "level": "INFO", 
    }, 
 }, 
 "handlers": { 
    "django_file": { 
        "class": " logging.handlers.RotatingFileHandler", 
        "filename": "path/to/django_logs.log", 
        "maxBytes": 1024 * 1024 * 10, # 10MB 
        "backupCount": 10, 
        "formatter": "verbose" 
    }, 
 }, 
}
```

### Working with Metrics and Events using NRQL

## Integrating messaging tools Using Slack message actions

## Handling production incidents betters

## Learning Blameless RCA for incidents

