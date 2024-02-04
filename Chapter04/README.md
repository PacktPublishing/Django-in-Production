# Chapter 4: Exploring Django Admin and Management Commands

## Table of Contents
* [Exploring Django Admin](#exploring-django-admin)
  * [Creating a superuser in Django](#creating-a-superuser-in-django)
  * [Understanding the Django admin interface](#understanding-the-django-admin-interface)
* [Customizing Django Admin](#customizing-django-admin)
  * [Adding Custom fields](#adding-custom-fields)
  * [Using filter_horizontal](#using-filter_horizontal)
  * [Using get_queryset](#using-get_queryset)
  * [Using third-party packages and themes](#using-third-party-packages-and-themes)
  * [Using Django Admin logs](#using-django-admin-logs)
* [Optimizing Django Admin for Production](#optimizing-django-admin-for-production)
  * [Renaming admin URLs](#renaming-admin-urls)
  * [Using 2FA for Admin users](#using-2fa-for-admin-users)
  * [Using Custom Admin Paginator](#using-custom-admin-paginator)
  * [Disabling ForeignKey drop-down options](#disabling-foreignkey-drop-down-options)
  * [Using list_select_related](#using-list_select_related)
  * [Overriding get_queryset for performance](#overriding-get_queryset-for-performance)
  * [Adding django-json-widget](#adding-django-json-widget)
  * [Using custom actions](#using-custom-actions)
  * [Using Permissions for Django Admin](#using-permissions-for-django-admin)
* [Creating Custom Management Commands](#creating-custom-management-commands)



## Exploring Django Admin

### Creating a superuser in Django

Follow the wizard to create a superuser:
```bash
$ python manage.py createsuperuser
```

### Understanding the Django admin interface

```python
from django.contrib import admin
from blog import models

class BlogAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Blog, BlogAdmin)

```

```python
from django.contrib import admin
from blog import models

class BlogCustomAdmin(admin.ModelAdmin):
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'created_at']
    date_hierarchy = 'created_at'

admin.site.register(models.Blog, BlogCustomAdmin)

```

## Customizing Django Admin


### Adding Custom fields

```python
class BlogCustom2Admin(admin.ModelAdmin):
    list_display = ('title', 'word_count', 'id')

    def word_count(self, obj):
        return obj.content.split()

admin.site.register(models.Blog, BlogCustom2Admin)
```

### Using filter_horizontal

```python
class BlogCustom3Admin(admin.ModelAdmin):
    filter_horizontal = ['tags']

admin.site.register(models.Blog, BlogCustom3Admin)
```

### Using get_queryset 

```python
class BlogCustom4Admin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'author_full_name']

    def author_full_name(self, obj):
        return f'{obj.author.user.first_name} {obj.author.user.last_name}'

    def get_queryset(self, request):
        default_qs = super().get_queryset(request)
        improved_qs = default_qs.select_related('author', 'author__user')
        return improved_qs
admin.site.register(models.Blog, BlogCustom4Admin)
```

### Using third-party packages and themes

### Using Django Admin logs 

```python
from django.contrib.admin.models import LogEntry

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False
```


## Optimizing Django Admin for Production

### Renaming admin URLs

### Using 2FA for Admin users

### Using Custom Admin Paginator

```python
from django.core import paginator
from django.utils.functional import cached_property

# Idea referred from
# https://hakibenita.com/optimizing-the-django-admin-paginator
class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999

class BlogCustom5Admin(admin.ModelAdmin):
    paginator = CustomPaginator
    
admin.site.register(models.Blog, BlogCustom5Admin)
```

### Disabling ForeignKey drop-down options

```python
class BlogCustom6Admin(admin.ModelAdmin):
    raw_id_fields = ('author',)
admin.site.register(models.Blog, BlogCustom6Admin)
```

### Using list_select_related

```python
class BlogCustom7Admin(admin.ModelAdmin):
    list_display = ['title', 'created_at', 'author_full_name']
    list_select_related = ['author', 'author__name']

    def author_full_name(self, obj):
        return obj.author.name
    
admin.site.register(models.Blog, BlogCustom7Admin)
```

### Overriding get_queryset for performance

### Adding django-json-widget

Install the package:
```bash
$ pip install django-json-widget
```


### Using custom actions

```python
class BlogCustom8Admin(admin.ModelAdmin):
    actions = ('print_blogs_titles',)

    @admin.action(description='Prints title')
    def print_blogs_titles(self, request, queryset):
        for data in queryset.all():
            print(data.title)
admin.site.register(models.Blog, BlogCustom8Admin)
```

### Using Permissions for Django Admin

## Creating Custom Management Commands

Create a custom management command to print total number of blogs. Create a file `blog/management/commands/total_blogs.py` with the following content:

```python
from django.core.management.base import BaseCommand
from blog.models import Blog

class Command(BaseCommand):
    help = 'Returns total number of blogs'

    def handle(self, *args, **options):
        total_blogs = Blog.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total blogs: "{total_blogs}"'))
```

now run the command:

```bash
$ python manage.py total_blogs
```

Now, let create a custom command that takes an argument and also prints total blogs. Create a file `blog/management/commands/custom_command_info.py` with the following content:

```python
class Command(BaseCommand):
    help = 'Returns total number of blogs'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('custom_inputs', nargs='+', type=int)

        # Named (optional) arguments
        parser.add_argument(
            '--custom',
            type=int,
            help='custom optional param',
        )

    def handle(self, *args, **options):
        print(f'Custom inputs - {options["custom_inputs"]}')
        print(f'Custom - {options["custom"]}')
        total_blogs = Blog.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Total blogs: "{total_blogs}"'))
```

now run the command:

```bash
$ python manage.py custom_command_info 1 2 3 --custom=4

OUTPUT 
Custom inputs - [1, 2, 3]
Custom - 4
Total blogs: "4"
```
