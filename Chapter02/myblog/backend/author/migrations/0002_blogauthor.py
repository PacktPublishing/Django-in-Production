# Generated by Django 5.0 on 2024-02-03 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BlogAuthor',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('author.author',),
        ),
    ]
