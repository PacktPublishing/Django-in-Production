from django.dispatch import receiver
from blog import signals


@receiver(signals.notify_author)
def send_email_to_author(sender, blog_id, **kwargs):
    # Sends email to author
    print('sending email to author logic', blog_id, kwargs)
