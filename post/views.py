from .models import Post, PostFile, Hashtag
from rest_framework import pagination, viewsets
from .serializers import PostSerializer, PostFileSerializer, HashtagSerializer

class PostPagination(pagination.PageNumberPagination):
    page_size = 10

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.exclude(is_deleted=True).order_by('-timestamp')
    serializer_class = PostSerializer
    pagination_class = PostPagination

class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer

class HashtagViewSet(viewsets.ModelViewSet):
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
