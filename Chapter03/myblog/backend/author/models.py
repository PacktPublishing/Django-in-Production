from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField()

    def fetch_short_bio(self):
         return self.bio[:100]

    def __str__(self):
        return self.name
