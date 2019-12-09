from rest_framework import serializers
from .models import Post, PostFile

class PostFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'post_id']


class PostSerializer(serializers.HyperlinkedModelSerializer):
    files = PostFileSerializer(source='postfile_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'files']

    def create(self, validated_data):
        files_data = self.context.get('view').request.FILES
        post = Post.objects.create(title=validated_data.get('title'),content=validated_data.get('content'))
        for file_data in files_data.values():
            PostFile.objects.create(post=post, file=file_data)
        return post
