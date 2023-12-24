from django.utils import timezone

from blog import signals
from blog.models import Blog

def publish_blog(blog_id):
    # publish blog logic to notify author
    signals.notify_author.send(sender=None, blog_id=blog_id)

def check_if_allowed_to_publish_blog(author):
    # check if author is allowed to publish blog
    blog_count_for_today = Blog.objects.filter(author_id=author.id, created_at__date=timezone.now().date()).count()
    return blog_count_for_today < 10
