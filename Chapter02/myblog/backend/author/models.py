from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    # demo_field = models.TextField(default='demo')  # Uncomment this line to test fake migrations
    email = models.EmailField()
    bio = models.TextField()

    def __str__(self):
        return self.name
    

class BlogAuthor(Author):
    class Meta:
        proxy = True
    
    def perform_something(self):
        pass
