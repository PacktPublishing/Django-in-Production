# Generated by Django 4.2 on 2023-12-02 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_coverimage_tag_alter_blog_author_blog_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='blog',
            options={'permissions': [('update_title', 'Can update the title of the blog'), ('update_content', 'Can update the content of blog')]},
        ),
    ]
