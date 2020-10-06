from django.utils import timezone
from django.db import models


def user_path(instance, filename):
    return f'user_{instance.instauser.id}/{filename}'


class Post(models.Model):
    photo = models.ImageField(upload_to=user_path, width_field=models.IntegerField, height_field=models.IntegerField, max_length=100)
    caption = models.CharField(max_length=250)
    date = models.DateTimeField(default=timezone.now)
    location = models.CharField(max_length=100, null=True, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
