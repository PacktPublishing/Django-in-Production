from blog import signals


def publish_blog(blog_id):
    # publish blog logic to notify author
    signals.notify_author.send(sender=None, blog_id=blog_id)
