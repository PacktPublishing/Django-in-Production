from author.models import Author
from blog.models import Blog
from blog.models import CoverImage

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
        'author': 'john@gmail.com',
        'cover_image': 'https://www.google.com/2'
    },
    {
        'title': 'Django is cool',
        'content': 'Django is cool',
        'author': 'jane@gmail.com',
        'cover_image': 'https://www.google.com/3'
    },
    {
        'title': 'Django is better than Flask',
        'content': 'Django is better than Flask',
        'author': 'jane@gmail.com',
        'cover_image': 'https://www.google.com/1'
    }
]

cover_image = [
    {
        'image_link': 'https://www.google.com/1'
    },
    {
        'image_link': 'https://www.google.com/2'
    },
    {
        'image_link': 'https://www.google.com/3'
    }
]

for author in author_data:
    Author.objects.get_or_create(email=author['email'], defaults={**author})

for image in cover_image:
    CoverImage.objects.get_or_create(image_link=image['image_link'], defaults={**image})

for blog in blog_data:
    author = Author.objects.get(email=blog['author'])
    cover_image = CoverImage.objects.get(image_link=blog['cover_image'])
    data = {**blog, 'author': author, 'cover_image': cover_image}
    Blog.objects.get_or_create(title=blog['title'], defaults={**data})
