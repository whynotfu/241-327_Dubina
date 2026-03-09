from rest_framework import viewsets
from .models import VideoGame
from .serializers import VideoGameSerializer


class VideoGameViewSet(viewsets.ModelViewSet):
    queryset = VideoGame.objects.all()
    serializer_class = VideoGameSerializer
