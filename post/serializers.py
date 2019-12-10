from rest_framework import serializers
from .models import Post, PostFile, Hashtag
import json

class HashtagSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id', 'url', 'name']

class PostFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'url', 'file', 'type', 'post_id']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    files = PostFileSerializer(source='postfile_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'url', 'title', 'content', 'files', 'hashtags', 'timestamp']

    def create(self, validated_data):
        #create post
        post = Post.objects.create(
            title=validated_data.get('title'),
            content=validated_data.get('content')
        )

        #handle hashtags
        hashtags_data = []
        if "hashtags_data" in dict(self.context.get('view').request.POST):
            hashtags_data = json.loads(self.context.get('view').request.POST['hashtags_data'])

        existing_hashtag_list = []
        for h_data in Hashtag.objects.all():
            existing_hashtag_list.append(h_data.name)

        hashtags = []
        for h_data in hashtags_data:
            if not h_data in existing_hashtag_list:
                Hashtag.objects.create(name=h_data)
            hashtags.append(Hashtag.objects.filter(name=h_data)[0])

        post.hashtags.set(hashtags)

        #Handle files
        files_data = self.context.get('view').request.FILES
        for file_data in files_data.values():
            PostFile.objects.create(post=post,type=str(file_data).split('.')[-1],file=file_data)

        return post

    def update(self, instance, validated_data):
        #post
        instance.title=validated_data.get('title')
        instance.content=validated_data.get('content')

        #hashtags
        hashtags_data = []
        if "hashtags_data" in dict(self.context.get('view').request.POST):
            hashtags_data = json.loads(self.context.get('view').request.POST['hashtags_data'])

        existing_hashtag_list = []
        for h_data in Hashtag.objects.all():
            existing_hashtag_list.append(h_data.name)

        hashtags = []
        for h_data in hashtags_data:
            if not h_data in existing_hashtag_list:
                Hashtag.objects.create(name=h_data)
            hashtags.append(Hashtag.objects.filter(name=h_data)[0])

        instance.hashtags.set(hashtags)

        #files
        files_data = self.context.get('view').request.FILES
        for file_data in files_data.values():
            PostFile.objects.create(post=instance,type=str(file_data).split('.')[-1],file=file_data)

        return instance
