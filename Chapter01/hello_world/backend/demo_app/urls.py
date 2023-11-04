from django.urls import path
from demo_app import views

urlpatterns = [
    path('hello-world/', views.hello_world),

    # This is the new line we added for "Linking app views using urls.py" section
    path('hello-world-drf/', views.hello_world_drf),

    # Next 3 line we added for "Use API Versioning" section
    path('demo-version/', views.demo_version),
    path('custom-version/', views.DemoView.as_view()),
    path('another-custom-version/', views.AnotherView.as_view()),

    # This is the new line we added for "Working with Views using DRF"-> "Class Based Views" -> "APIView" section
    path('apiview-class/', views.DemoAPIView.as_view())
]
