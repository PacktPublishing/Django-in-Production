from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    user = models.OneToOneField(User, on_delete=models.PROTECT)


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

# class CoverImage(BaseTimeStampModel):
#     image_link = models.URLField()
#     blog = models.OneToOneField(Blog, related_name='blog_ci', on_delete=models.PROTECT)

class Tags(BaseTimeStampModel):
    name = models.CharField(max_length=100)

class Blog(BaseTimeStampModel):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(Author, related_name='author_blogs', on_delete=models.PROTECT)
    tags = models.ManyToManyField(Tags)


# author = models.Author.objects.get(email='argo@thetldr.tech')
# all_blogs_by_an_author = author.blog_set.all()
# selected_blog = author.blog_set.filter(title='first blog')
#
#
# @database_debug
# def regular_query():
#     blogs = models.Blog.objects.all()
#     return [blog.author.first_name for blog in blogs]
#
# @database_debug
# def select_related_query():
#     blogs = models.Blog.objects.select_related('author').all()
#     return [blog.author.first_name for blog in blogs]
#
# @database_debug
# def prefetch_related_query():
#     blogs = models.Blog.objects.prefetch_related('author').all()
#     return [blog.author.first_name for blog in blogs]
#


# class Author(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     bio = models.TextField()
#
#     def get_short(self):
#          return self.bio[:100]
