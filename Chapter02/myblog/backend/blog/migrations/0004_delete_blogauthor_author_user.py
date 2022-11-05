# Generated by Django 4.0 on 2022-07-03 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('blog', '0003_blogauthor_blog_created_at_blog_updated_at_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BlogAuthor',
        ),
        migrations.AddField(
            model_name='author',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='auth.user'),
            preserve_default=False,
        ),
    ]
