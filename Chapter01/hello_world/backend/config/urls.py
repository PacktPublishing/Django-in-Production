"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import include
from django.urls import path


def hello_world(request):
    return HttpResponse('hello world')


urlpatterns = [
    path('admin/', admin.site.urls),
    # This is the line we added for "Creating our Django hello_world Project" section
    path('hello-world', hello_world),

    # This is the new line we added for "Linking app views using urls.py" section
    path('demo-app/', include('demo_app.urls')),

    # This is the new line we added for "Use API Versioning" section
    path('<version>/demo-app-version/', include('demo_app.urls')),
]
