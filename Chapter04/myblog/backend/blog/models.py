from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100, unique=True)
    content = models.TextField()
    author = models.ForeignKey('author.Author', related_name='author_blogs', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    cover_image = models.OneToOneField('CoverImage', related_name='blog_cover_image', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', related_name='blog_tags')

    def __str__(self):
        return self.title


class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()


class Tag(BaseTimeStampModel):
    name = models.CharField(max_length=100, unique=True)
