from author.models import Author
from blog.models import Blog

author_data = [
    {
        'name': 'John Doe',
        'email': 'john@gmail.com',
        'bio': 'Python Blogger'
    },
    {
        'name': 'Jane Doe',
        'email': 'jane@gmail.com',
        'bio': 'Django Blogger'
    }
]

blog_data = [
    {
        'title': 'Python is cool',
        'content': 'Python is cool',
        'author': 'john@gmail.com'
    },
    {
        'title': 'Django is cool',
        'content': 'Django is cool',
        'author': 'jane@gmail.com'
    },
    {
        'title': 'Django is better than Flask',
        'content': 'Django is better than Flask',
        'author': 'jane@gmail.com'
    }
]

for author in author_data:
    Author.objects.create(**author)

for blog in blog_data:
    author = Author.objects.get(email=blog['author'])
    data = {**blog, 'author': author}
    Blog.objects.create(**data)
