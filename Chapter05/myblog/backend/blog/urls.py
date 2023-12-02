from django.urls import path

from blog import views


urlpatterns = [
    path('perm-check/', views.update_blog_title)
]
