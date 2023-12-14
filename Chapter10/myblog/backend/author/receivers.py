from django.dispatch import receiver
from django.db.models.signals import post_save

from blog import signals
from author.models import Author


@receiver(signals.notify_author)
def send_email_to_author(sender, blog_id, **kwargs):
    # Sends email to author
    print('sending email to author logic', blog_id, kwargs)


@receiver(post_save, sender=Author)
def my_handler(sender, **kwargs):
    print("Signal called")
