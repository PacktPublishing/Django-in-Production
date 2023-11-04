from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response


from blog import models


@api_view(['POST'])
def create_blog(request):
    ...
    blogs_count = models.Blog.objects.count()
    # log_event(event_name='total_blog', log_data={'count': blogs_count})
    ...
    return Response(data={})

# first_blog = models.Blog.objects.all()
# new_blog = serializers.BlogSerializer(instance=first_blog)


def get_all_blogs(author_id):
    blogs = models.Blog.objects.filter(author_id=author_id)
    return list(blogs)

CACHEOPS = {
    # Automatically cache any User.objects.get() calls for 15 minutes
    # This also includes .first() and .last() calls,
    # as well as request.user or post.author access,
    # where Post.author is a foreign key to auth.User
    'auth.user': {'ops': 'get', 'timeout': 60*15},

    # Automatically cache all gets and queryset fetches
    # to other django.contrib.auth models for an hour
    'auth.*': {'ops': {'fetch', 'get'}, 'timeout': 60*60}
}

# from rest_framework.throttling import UserRateThrottle
#
# from rest_framework.views import APIView
# from rest_framework.throttling import AnonRateThrottle
#
#
# class BlogApiView(APIView):
#     throttle_classes = [AnonRateThrottle]

# def