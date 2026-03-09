from rest_framework import serializers
from .models import VideoGame


class VideoGameSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoGame
        fields = '__all__'
