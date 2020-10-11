from django.utils import timezone
from django.db import models
from instauser.models import InstaUser


class Post(models.Model):
    photo = models.ImageField(upload_to="image")
    caption = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    author = models.ForeignKey(InstaUser, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.author}.post-{self.pk}'


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    creator = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.text
