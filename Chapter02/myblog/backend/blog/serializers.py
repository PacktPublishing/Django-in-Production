# from django.db.backends.signals import connection_created
# from django.dispatch import receiver
from rest_framework import serializers, validators
# from .models import Blog, Author
#
# @receiver(connection_created)
# def setup_timeout(connection, **kwargs):
#     # Set Timeout for every statement as 30 seconds.
#     with connection.cursor() as cursor:
#         cursor.execute("SET statement_timeout TO 30000;")
#
# # class Blog(BaseTimeStampModel):
# #     title = models.CharField(max_length=200)
# #     content = models.TextField()
# #     author = models.ForeignKey(Author, related_name='author_blogs', on_delete=models.PROTECT)
# #
#
# def demo_func_validator(attr):
#     print('func val')
#     if '_' in attr:
#         raise serializers.ValidationError('Title cannot contain underscore(_)')
#     return attr
#
# def custom_obj_validator(attrs):
#     print('custom object validator')
#     if attrs['title'] == attrs['content']:
#         raise serializers.ValidationError('Title and content are same')
#     return attrs
#
# class BlogSerializer(serializers.ModelSerializer):
#     def to_internal_value(self, data):
#         print(self.context)
#         return super(BlogSerializer, self).to_internal_value(data)
#     def validate(self, attrs):
#         print(self.context)
#         print('cl')
#         if attrs['title'] == attrs['content']:
#             raise serializers.ValidationError('Title and content are same')
#         return attrs
#
#     class Meta:
#         model = Blog
#         fields = '__all__'
#
# class AuthorSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Author
#         fields = '__all__'
#
# update_input_data = {
#     'title': 'updated blog title',
# }
# # existing_blog = models.Blog.objects.get(id=10)
# # new_blog = BlogSerializer(instance=existing_blog, data=update_input_data, partial=True)
# # if new_blog.is_valid():
# #     new_blog.save()
# # else:
# #     print(new_blog.errors)
#
# # "ffmpeg -i https://didcj2cylf4ls.cloudfront.net/3ffad50123470b00fe3e292a83bd3677a0006b0c38fbe2c85e52a6945de0bb30/7m1KLQQbOTw1jbWSkX8CQ_master-part.m3u8 -c copy abcdef.mkv -preset ultrafast"
# #
# # class BlogSerialzier(serializers.ModelSerializer):
# #     author = serializers.PrimaryKeyRelatedField(
# #         queryset=Author.objects.all()
# #     )
# #     tags = serializers.PrimaryKeyRelatedField(
# #         queryset=Tags.objects.all(), many=True
# #     )
# #     cover_image = serializers.PrimaryKeyRelatedField(
# #         queryset=CoverImage.objects.all(),
# #         validators=[validators.UniqueValidator(CoverImage.objects.all())]
# #     )
# #
# #     class Meta:
# #         model = Blog
# #         fields = '__all__'
#
# class BlogAuthorSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = Author
#         fields = ['name', 'bio']
#
# class BlogSerialzier(serializers.ModelSerializer):
#     tags = CustomPKRelatedField(queryset=Tags.objects.all())
#
#     class Meta:
#         model = Blog
#         fields = '__all__'
#
# # class AuthorSerializer(serializers.ModelSerializer):
# #     long_bio = serializers.CharField(source='bio')
# #     short_bio = serializers.CharField(source='fetch_short_bio')
# #     author_first_name = serializers.CharField(source='user.first_name')
# #
# #     class Meta:
# #         model = Author
# #         fields = '__all__'
#
# # class BlogSerializer(serializers.ModelSerializer):
# #     def to_representation(self, instance):
# #         resp = super().to_representation(instance)
# #         resp['title'] = resp['title'].upper()
# #         return resp
# #
# #     class Meta:
# #         model = Blog
# #         fields = '__all__'
# # from rest_framework import views
# # from rest_framework import response
# # from rest_framework import filters
# #
# # class BlogGetCreateView(views.APIView):
# #     def get(self, request):
# #         blogs_obj_list = Blog.objects.all()
# #         blogs = BlogSerialzier(blogs_obj_list, many=True)
# #         return Response(blogs.data)
# #     def post(self, request):
# #         input_data = request.data
# #         blog_obj = BlogSerialzier(data=input_data)
# #         if blog_obj.is_valid():
# #            blog_obj.save()
# #            return Response(blog_obj.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day'
    }
}