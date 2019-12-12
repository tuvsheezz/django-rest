from .models import Post, PostFile, Hashtag
from rest_framework import viewsets
from .serializers import PostSerializer, PostFileSerializer, HashtagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-timestamp')
    serializer_class = PostSerializer

class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
