from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey('author.Author', related_name='author_blogs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('Tags', related_name='blog_tags')

    def __str__(self):
        return self.title


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()

class Tags(BaseTimeStampModel):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name