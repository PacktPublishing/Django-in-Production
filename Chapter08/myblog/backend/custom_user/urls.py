from django.urls import path

from custom_user import views


urlpatterns = [
    path('login/', views.login)
]
