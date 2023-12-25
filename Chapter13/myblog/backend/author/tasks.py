from celery.schedules import crontab

from config.celery import app
from config.celery import task


@app.on_after_finalize.connect
def setup_basic_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
       crontab(),
       demo_task.s("periodic task")
    )

@task(bind=True)
def demo_task(self, value):
    print(value)
