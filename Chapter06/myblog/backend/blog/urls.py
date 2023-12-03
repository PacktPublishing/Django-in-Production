from django.urls import path

from blog import views


urlpatterns = [
    path('find-by-author/', views.get_blogs_by_author),
    path('perm-check/', views.update_blog_title),
]
