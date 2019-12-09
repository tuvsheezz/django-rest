from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return self.title

class PostFile(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    file = models.FileField(upload_to='post_files', blank=True)
