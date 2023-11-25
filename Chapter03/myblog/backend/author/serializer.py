from rest_framework import serializers

from author import models
class AuthorSerializer(serializers.ModelSerializer):
    long_bio = serializers.CharField(source='bio')
    short_bio = serializers.CharField(source='fetch_short_bio')

    class Meta:
        model = models.Author
        fields = '__all__'
        exclude = ['bio', 'user']
