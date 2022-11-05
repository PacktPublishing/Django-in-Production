from django.db import models
from django.utils import timezone
from django.db import connection

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True, default=timezone.now)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['last_name']),
        ]


class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    bio = models.TextField()

    class Meta:
        indexes = [
            models.Index(fields=['last_name']),
        ]

    def get_author_name(self):
        return f'{self.first_name} {self.last_name}'

    def get_short_bio(self):
        return f'{self.bio[:200]}...'
