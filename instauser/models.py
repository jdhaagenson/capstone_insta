from django.db import models
from django.contrib.auth.models import AbstractUser


class InstaUser(AbstractUser):
    display_name = models.CharField(max_length=40, unique=False)
    bio = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, blank=True, default='self')
    profile_pic = models.ImageField(upload_to='image', default='/static/images/blank_user.jpg', blank=True, null=True)
    theme = models.CharField(max_length=50, blank=True, null=True, default='default')

    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f"@{self.username}"


class Theme(models.Model):
    holiday = models.CharField(max_length=50)
    pattern = models.CharField(max_length=250)
    font = models.CharField(max_length=50)
    color_scheme = models.CharField(max_length=50)
