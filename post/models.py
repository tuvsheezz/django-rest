from django.db import models

# Create your models here.

class Hashtag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    hashtags = models.ManyToManyField(Hashtag, blank=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files', blank=True)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type
