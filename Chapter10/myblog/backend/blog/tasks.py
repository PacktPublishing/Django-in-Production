from config.celery import task

@task(bind=True)
def send_email_to_followers(self, author_id, blog_id):
    print(f"Sending email to followers of author {author_id} for blog {blog_id}")