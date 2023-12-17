from django.urls import path

from blog import views


urlpatterns = [
    path('find-by-author/', views.get_blogs_by_author),
    path('perm-check/', views.update_blog_title),
    path('unpaginated/', views.get_blog_without_pagination),
    path('paginated/', views.get_blog_with_pagination),
    path('publish/', views.publish_blog),
    path('verify/', views.verify_blog),
    path('hello-world/', views.hello_world, name='hello_world'),
    path('hello-world-2/', views.hello_world_2, name='hello_world_2'),
]
