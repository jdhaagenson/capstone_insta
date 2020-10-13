from django.db import models
from django.contrib.auth.models import AbstractUser


class InstaUser(AbstractUser):
    display_name = models.CharField(max_length=40, unique=False)
    bio = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, default='self')
    profile_pic = models.ImageField(upload_to='image', default='/media/image/default.jpg')
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f"@{self.username}"
