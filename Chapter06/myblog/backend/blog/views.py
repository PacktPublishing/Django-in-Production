from django.http import HttpResponse

from cacheops import cached
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import ScopedRateThrottle

from blog.models import Blog
from blog.serializers import BlogSerializer
from common.logging_util import log_event


def update_blog_title(request):
    blog_id = request.GET.get('id')
    blog = Blog.objects.get(id=blog_id)
    if request.user.has_perm("blog.update_title"):
        # perform operation
        return HttpResponse('User has permission to update title')
    return HttpResponse('User does not have permission to update title')


def check_permission(user, group_name):
    return user.groups.filter(name=group_name).exists()


@api_view(['POST'])
def blog_view(request):
    if not check_permission(request.user, 'can_view_blog'):
        return Response(status=403)
    print('User has permission to view blog')
    return Response(status=200)


# Cache the result of this function for 10 minutes, it would be unique for each author_id.
@cached(timeout=60*10)
def get_all_blogs(author_id):
    print('Fetching blogs from database')
    blogs = Blog.objects.filter(author_id=author_id)
    blogs_data = BlogSerializer(blogs, many=True).data
    return blogs_data


def demo():
    log_event('demo', {'author_id': 1})


@api_view(['GET'])
def get_blogs_by_author(request):
    author_id = request.GET.get('author_id')
    blogs = get_all_blogs(author_id)
    log_event('get_blogs_by_author', {'author_id': author_id})
    demo()
    return Response({'blogs': blogs})


# Throttling anonymous users.
class BlogApiView(APIView):
    throttle_classes = [AnonRateThrottle]

    def get(self, request):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class Blog2ApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog_limit'

    def get(self, request):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class BlogDetailApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog_limit'

    def get(self, request):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)


class Blog3ApiView(APIView):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'blog_2_limit'

    def get(self, request):
        content = {
            'status': 'request was permitted'
        }
        return Response(content)
