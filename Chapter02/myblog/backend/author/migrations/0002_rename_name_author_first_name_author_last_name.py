# Generated by Django 4.0 on 2022-06-11 07:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='author',
            name='last_name',
            field=models.CharField(default='a', max_length=100),
            preserve_default=False,
        ),
    ]
