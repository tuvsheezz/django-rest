## Django-rest-framework turshsan temdeglel

Ene udaad olon zurag/file-tai post oruulj boldog bolgoy.
p.s:

### Clone hiigeed ajilluulah gej baigaa bol

```
$ git clone ...
$ cd restapi
$ git checkout manytomany
$ pip install requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

### Esvel daraah alhamuudaar shineer uusgej bolomjtoi

#### Step 0
Hervee oilgomjgui baival ```uploadmultiimage``` branch-g checkout hiigeed turshij uzeerei.
```
$ git clone ...
$ cd restapi
$ git checkout uploadmultiimage
```

#### Step 1 Model uusgeh
Postondoo hashtag oruulhiin tuld Hashtag model bol Post model ManyToManyField nemsen.

```
from django.db import models

# Create your models here.

class Hashtag(models.Model):                    #nemsen
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag)      #nemsen
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files', blank=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type
```

###### DB shalgah
```
sqlite> .header on
sqlite> .mode column
sqlite> .tables
    # auth_group                  django_content_type       
    # auth_group_permissions      django_migrations         
    # auth_permission             django_session            
    # auth_user                   post_hashtag          #nemegdsen    
    # auth_user_groups            post_post             
    # auth_user_user_permissions  post_post_hashtags    #nemegdsen    
    # django_admin_log            post_postfile     

sqlite> pragma table_info('post_post');
    # cid         name        type        notnull     dflt_value  pk        
    # ----------  ----------  ----------  ----------  ----------  ----------
    # 0           id          integer     1                       1         
    # 1           title       varchar(10  1                       0         
    # 2           content     text        1                       0         
    # 3           timestamp   datetime    1                       0         

sqlite> pragma table_info('post_hashtag');
    # cid         name        type        notnull     dflt_value  pk        
    # ----------  ----------  ----------  ----------  ----------  ----------
    # 0           id          integer     1                       1         
    # 1           name        varchar(50  1                       0         

sqlite> pragma table_info('post_post_hashtags');
    # cid         name        type        notnull     dflt_value  pk        
    # ----------  ----------  ----------  ----------  ----------  ----------
    # 0           id          integer     1                       1         
    # 1           post_id     integer     1                       0         
    # 2           hashtag_id  integer     1                       0          
```

ManyToManyField genguut 2 modeliin relation table-iig uuru uusgechihdeg ym baina.
ene udaad bol ```post_post_hashtags``` gesen nerteigeer uussn baina.

#### Step 2 Serializer

Post-iin tag-g ["tag1", "tag2", "tag3"] helbereer bicheed yvuuldag, teriig n shalgaad DB-d burtgeltei tag baival shuud, ugui bol shineer burtgeed postond tagiig burtgedeg.
File n bol shuud ordog

Update hiihed mun ["tag1", "tag2", "tag3"] helbereer tag-aa avaad adilhan nuhtsuluur burtgedeg.
File n nemegdeed yvj baigaa. yr n bol daraa n file ustgadag ym hiinee.

```
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
```


#### Step 3 Views

```
from .models import Post, PostFile, Hashtag #import Hashtag model
from rest_framework import viewsets
from .serializers import PostSerializer, PostFileSerializer, HashtagSerializer #import HashtagSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer

class HashtagViewSet(viewsets.ModelViewSet): #add HashtagViewSet
    queryset = Hashtag.objects.all()
    serializer_class = HashtagSerializer
```

#### Step 4 Routes

restapi/urls.py -d
```
router.register(r'api/hashtags', views.HashtagViewSet)
```
