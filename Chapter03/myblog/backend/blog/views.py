from rest_framework import views
from rest_framework import response
from rest_framework import generics
from rest_framework import status
from rest_framework import filters
from blog import models
from blog import serializers as serializer


# Create your views here.

class BlogGetCreateView(views.APIView):
    def get(self, request):
        blogs_obj_list = models.Blog.objects.all()
        blogs = serializer.BlogSerializer(blogs_obj_list, many=True)
        return response.Response(blogs.data)

    def post(self, request):
        input_data = request.data
        b_obj = serializer.BlogSerializer(data=input_data)
        if b_obj.is_valid():
            b_obj.save()
            return response.Response(b_obj.data, status=status.HTTP_201_CREATED)
        return response.Response(b_obj.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogGetUpdateView(generics.ListCreateAPIView):
    serializer_class = serializer.BlogSerializer

    def get_queryset(self):
        blogs_queryset = models.Blog.objects.filter(id__gt=1)
        return blogs_queryset


class BlogGetUpdateFilterView(generics.ListAPIView):
    serializer_class = serializer.BlogSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['title']
