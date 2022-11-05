from django.contrib import admin
from blog.models import Blog, Tags, Author


from django.db import connection
from django.db import reset_queries


def database_debug(func):
    def inner_func(*args, **kwargs):
        reset_queries()
        results = func()
        query_info = connection.queries
        print('function_name: {}'.format(func.__name__))
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return results
    return inner_func

from django.core import paginator
from django.utils.functional import cached_property

class CustomPaginator(paginator.Paginator):
    @cached_property
    def count(self):
        return 9999999999
# Courtesy- https://hakibenita.com/optimizing-the-django-admin-paginator

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    paginator = CustomPaginator
    raw_id_fields = ('author',)
    search_fields = ['title']
    show_full_result_count = True
    list_filter = ['title']
    list_display = ['title', 'created_at', 'author_full_name']
    list_select_related = ['author', 'author__user']
    actions = ('print_blogs_titles',)


    @admin.action(description='Prints title')
    def print_blogs_titles(self, request, queryset):
        for data in queryset.all():
            print(data.title)

    def author_full_name(self, obj):
        reset_queries()

        response = f'{obj.author.user.first_name} {obj.author.user.last_name}'
        query_info = connection.queries
        print('query_count: {}'.format(len(query_info)))
        queries = ['{}\n'.format(query['sql']) for query in query_info]
        print('queries: \n{}'.format(''.join(queries)))
        return response

    # def get_queryset(self, request):
    #     default_qs = super().get_queryset(request)
    #     improved_qs = default_qs.select_related('author', 'author__user')
    #     return improved_qs


    list_per_page = 30

    date_hierarchy = 'created_at'
    filter_horizontal = ['tags']

@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    pass

# class Author(models.Model):
#     email = models.EmailField()
#     user = models.OneToOneField(User, on_delete=models.PROTECT)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('email', 'full_name', 'id')

    def full_name(self, obj):
        return f'{obj.user.first_name} {obj.user.last_name}'

from django.contrib.admin.models import LogEntry
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request):
        return False

