from django.db import models


class Blog(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey("author.Author", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Uncomment the below line to see the effect of migrations
    # demo_field = models.TextField(default='demo')
    cover_image = models.OneToOneField('CoverImage', related_name='blog_cover_image', on_delete=models.PROTECT)

    def __str__(self):
        return self.title
    

class BaseTimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True


class CoverImage(BaseTimeStampModel):
    image_link = models.URLField()
