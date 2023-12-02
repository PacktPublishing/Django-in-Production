from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from blog.models import Blog


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
