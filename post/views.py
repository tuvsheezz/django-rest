from .models import Post, PostFile
from rest_framework import viewsets
from .serializers import PostSerializer, PostFileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer
