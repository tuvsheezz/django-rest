## Django-rest-framework turshsan temdeglel

### Clone hiigeed ajilluulah gej baigaa bol

```
$ git clone ...
$ cd restapi
$ pip install requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

### Esvel daraah alhamuudaar shineer uusgej bolomjtoi

#### Step 0 Suulgasan baisan (minii ashigladag)
- python3
- pip3 (sudo apt get install -y python3-pip)
- virtualenv (pip3 install virtualenv)
- tree (sudo apt install tree) (project-iin structure-g oilgomjtoi harahad zugeer)
- sqlite3 (RDBMS)

#### Step 1 Zarim 1 ym hum hiih
Hussen gazraa (folder-uudiin neriig duraarai uguurei)

```sh
$ mkdir djangorest-test && cd djangorest-test
$ virtualenv -p python3 env
$ source env/bin/activate
$ mkdir restapi && cd restapi
$ pip install django djangorestframework django-cors-headers Pillow

```

#### Step 2 Shine django rest project uusgeh
```sh
$ django-admin startproject restapi .
$ cd restapi
$ tree
```
tree-iin ur dun
```
.
├── manage.py
└── restapi
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
```

#### Step 3 Project-n settings.py-g uurchluh

Daraagiin 2 muriig INSTALLED_APPS-d nemne.
```
INSTALLED_APPS = [
    ...,
    'rest_framework',
    'corsheaders',
]
```
Daraagiin 1 muriig MIDDLEWARE-d nemne
```
MIDDLEWARE = [
    ...,
    'corsheaders.middleware.CorsMiddleware',
]
```
Haana n ch ym 1 gazar n daraahiig nemne. Yvaandaa file ntr oruulj ntr bolhod zoriulaad cors media path ntr zarlaad baigaa ym hereggui bol cors suulgahgui media tohiruulahgui bj bolno.
```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
```

#### Step 4 Migrate hiih

```
$ python manage.py makemigrations
$ python manage.py migrate
```
admin, auth, contenttypes, sessions-iin migrate-uud orno.

migrate hiisnii daraa db.sqlite3 gesen file uusne. (DB)

```sh
$ sqlite3 db.sqlite3
sqlite3> .header on
sqlite3> .mode column
sqlite3> .tables
```

DB-ee neegeed header mode tohirgoo hiigeed (arai oilgomjtoi haragdah uchraas ) table list-g n harahad daraah baidaltai bolson baina.

```
auth_group                  django_admin_log          
auth_group_permissions      django_content_type       
auth_permission             django_migrations         
auth_user                   django_session            
auth_user_groups            auth_user_user_permissions                 
```
sqlite3-aas garahdaa .q

Super user ntr uusgej boldog l ym shig baina. Daraa n sudlaad oruulna.
```sh
python manage.py createsuperuser --email admin@example.com --username admin
```

#### Step 5 Shine app uusgeh
```sh
$ django-admin startapp post
$ tree
```
tree-iin ur dun.
```
.
├── manage.py
├── post
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── README.md
└── restapi
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```

#### Step 6 Shine app-aa settings.py-d burtgeh
```
INSTALLED_APPS = [
    ...,
    'post',
]
```


#### Step 7 Model class uusgeh

post/models.py-d modeloo nemne.
```
from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images')

    def __str__(self):
        return self.title
```

post/admin.py-d modeloo burtgene. Daraah 2 muriig nemhed l bolh bololtoi.

```
from .models import Post
admin.site.register(Post)
```

#### Step 8 Migrate hiih

```
$ python manage.py makemigrations post
$ python manage.py migrate post
```

Commanduudiig ariin post baihgui bsn ch bolno. ingej bichvel tuhain app-n migrations-g uusgeh, migrate hiih bolomjtoi ym baina.

sqlite3-aar db.sqlite3-g shalgahad daraah baidaltai buyu post_post gesn table nemegdsen baina.
```
auth_group                  django_admin_log          
auth_group_permissions      django_content_type       
auth_permission             django_migrations         
auth_user                   django_session            
auth_user_groups            post_post                 
auth_user_user_permissions
```

```
sqlite3>pragma table_info('post_post');

```
table-iin butets info-g harahad
```
cid         name        type        notnull     dflt_value  pk        
----------  ----------  ----------  ----------  ----------  ----------
0           id          integer     1                       1         
1           title       varchar(10  1                       0         
2           content     text        1                       0         
3           image       varchar(10  1                       0         
```
modeld bichsenii daguu uusgegdsen baih ystoi ntr hahaha.
(esvel zugeer ```.schema post_post``` gesen ch bolno.)

Project-iin structure n daraah baidaltai bolson baina

```
.
├── db.sqlite3
├── manage.py
├── post
│   ├── admin.py
│   ├── apps.py
│   ├── __init__.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   ├── __init__.py
│   │   └── __pycache__
│   │       ├── 0001_initial.cpython-37.pyc
│   │       └── __init__.cpython-37.pyc
│   ├── models.py
│   ├── __pycache__
│   │   ├── admin.cpython-37.pyc
│   │   ├── __init__.cpython-37.pyc
│   │   └── models.cpython-37.pyc
│   ├── serializers.py
│   ├── tests.py
│   └── views.py
├── README.md
└── restapi
    ├── __init__.py
    ├── __pycache__
    │   ├── __init__.cpython-37.pyc
    │   ├── settings.cpython-37.pyc
    │   └── urls.cpython-37.pyc
    ├── settings.py
    ├── urls.py
    └── wsgi.py

```
post-iin migration folder uuseed dotor n migrationuud n file helbereer baina. orood harj bolno.

#### Step 9 Model serializer uusgeh

```sh
$ touch post/serializers.py
```
post app-d serializers.py gesn file uusgeed daraah code-g oruulna.

```
from rest_framework import serializers
from .models import Post

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image']
```

#### Step 10 ViewSet
```
from .models import Post
from rest_framework import viewsets
from .serializers import PostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

```

#### Step 11 url-ee burtgeh

restapi/urls.py-d url burtgene daraah baidaltai bolno.

```
from django.urls import include, path
from rest_framework import routers
from post import views
from django.conf import settings
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register(r'api/posts', views.PostViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

```

Post maani image-tei uchraas static route nemj haruulh shaardlagatai uchraas
```
urlpatterns = [
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```
gesn butetstei bolson baigaa.

#### Step 12 Uur app nemeh bol Step 5-aas Step 11 hurtel hiigeel bhd boloh baih

#### Step 13 Test
```sh
python manage.py runserver
```
Open http://localhost:8000/api/posts
