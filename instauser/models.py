from django.db import models
from django.contrib.auth.models import AbstractUser


class InstaUser(AbstractUser):
    display_name = models.CharField(max_length=40, unique=False)
    bio = models.CharField(max_length=100, blank=True, null=True)
    followers = models.ManyToManyField("self", symmetrical=False, default='self')
    profile_pic = models.ImageField(default='/image/Screen_Shot_2019-09-13_at_12.40.32_PM.png', upload_to='image', blank=True)
    REQUIRED_FIELDS = ['display_name']

    def __str__(self):
        return f"@{self.username}"
