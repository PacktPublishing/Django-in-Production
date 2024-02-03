from factory import SubFactory, Sequence
from factory.django import DjangoModelFactory

from blog import models as blog_models
from author import models as author_models


class AuthorFactory(DjangoModelFactory):
    class Meta:
        model = author_models.Author

    name = Sequence(lambda n: f'Author {n}')
    email = Sequence(lambda n: f'a{n}@gmail.com')


class CoverImageFactory(DjangoModelFactory):
    class Meta:
        model = blog_models.CoverImage

    image_link = Sequence(lambda n: f'https://www.example.com/image/{n}')


class BlogFactory(DjangoModelFactory):
    class Meta:
        model = blog_models.Blog

    title = Sequence(lambda n: f'Blog {n}')
    content = Sequence(lambda n: f'Blog content {n}')
    author = SubFactory(AuthorFactory)
    cover_image = SubFactory(CoverImageFactory)