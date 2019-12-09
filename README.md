## Django-rest-framework turshsan temdeglel

Ene udaad olon zurag/file-tai post oruulj boldog bolgoy.
p.s:

### Clone hiigeed ajilluulah gej baigaa bol

```
$ git clone ...
$ cd restapi
$ git checkout uploadmultiimage
$ pip install requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

### Esvel daraah alhamuudaar shineer uusgej bolomjtoi

#### Step 0
Hervee oilgomjgui baival ```master``` branch-g checkout hiigeed turshij uzeerei.
```
$ git clone ...
$ cd restapi
$ git checkout master
```
CORS-iin tohirgoog daraa n uurchilnuu. gehdee 1 udaadaa
restapi/settings.py-d
```
CORS_ORIGIN_ALLOW_ALL = True
```
geed nemchihlee.

#### Step 1 Model uusgeh

Yunii umnu modeloo uurchlunu. post-file modeloo nemeed post modeloo uurchlunu.
post/models.py-d daraah hesgiig nemne. Post model-g jaahn uurchilsun.

```
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files', blank=True)
    type = models.CharField(max_length=100)

```

#### Step 2 admin.py-d burtgeh

post/admin.py
```
from django.contrib import admin
from .models import Post, PostFile

# Register your models here.

admin.site.register(Post)
admin.site.register(PostFile)
```

#### Step 3 Serializer uurchluh

post/serializers.py
```
from rest_framework import serializers
from .models import Post, PostFile

class PostFileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PostFile
        fields = ['id', 'file', 'type', 'post_id']

class PostSerializer(serializers.HyperlinkedModelSerializer):
    files = PostFileSerializer(source='postfile_set', many=True, read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'files', 'timestamp']

    def create(self, validated_data):
        files_data = self.context.get('view').request.FILES
        post = Post.objects.create(title=validated_data.get('title'),content=validated_data.get('content'))
        for file_data in files_data.values():
            PostFile.objects.create(post=post,type=str(file_data).split('.')[-1],file=file_data)
            print(file_data)
        return post
```

#### Step 4 ViewSet

Daraah uurchlultuudiig nemne
```
from .models import Post, PostFile
from rest_framework import viewsets
from .serializers import PostSerializer, PostFileSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class PostFileViewSet(viewsets.ModelViewSet):
    queryset = PostFile.objects.all()
    serializer_class = PostFileSerializer

```
#### Step 5 Route nemeh

project-iin urls.py buyu ene tohioldold restapi/urls.py-d daraah muriig nemne
```
...
router = routers.DefaultRouter()
router.register(r'api/posts', views.PostViewSet)
router.register(r'api/postfiles', views.PostFileViewSet) # ene muriig nemsen
...

```


#### Step 6 Migrate
```sh
$ python manage.py makemigrations
$ python manage.py migrate
```
#### Step 7 db shalgah

```
sqlite> .tables
    # auth_group                  django_admin_log          
    # auth_group_permissions      django_content_type       
    # auth_permission             django_migrations         
    # auth_user                   django_session            
    # auth_user_groups            post_post                 
    # auth_user_user_permissions  post_postfile

sqlite> pragma table_info('post_post');
    # cid         name        type        notnull     dflt_value  pk        
    # ----------  ----------  ----------  ----------  ----------  ----------
    # 0           id          integer     1                       1         
    # 1           title       varchar(10  1                       0         
    # 2           content     text        1                       0         
    # 3           timestamp   datetime    1                       0    


sqlite> pragma table_info('post_postfile');
    # cid         name        type        notnull     dflt_value  pk        
    # ----------  ----------  ----------  ----------  ----------  ----------
    # 0           id          integer     1                       1         
    # 1           file        varchar(10  1                       0         
    # 2           post_id     integer     1                       0         
    # 3           type        varchar(10  1                       0         

```
bolson baina.

#### Step 8 Test
1. postman-eer shalga uzlee. OK.

anhaarah zuil:
  new request -> body -> form data gej songood
  door garch irsen deer n murnuudee nemeed yvna.
  file-aa bolhoor file_1 file_2 file_3 gej nerleed fieldee file bolgoj songood request yvuulna.

2. db orson medeelel shalgay. OK

```
sqlite> select * from post_post where id = 7;
  # id          title       content     timestamp                 
  # ----------  ----------  ----------  --------------------------
  # 7           title       conte       2019-12-09 10:10:20.336079

sqlite> select * from post_postfile where post_id = 7;
  # id          file                                               post_id     type      
  # ----------  -------------------------------------------------  ----------  ----------
  # 7           post_files/Deep-Learning-with-PyTorch_Yu9Oigm.pdf  7           txt       
  # 8           post_files/example_yfGjscJ.txt                     7           txt       
```


P.S: 2 shirheg 1GB-iin file upload hiihed 1.54 min bolj baina.

http://localhost:8000/api/posts ruu orood shalgaad uzeerei.

### Next => Many to many relation
branch: manytomany
