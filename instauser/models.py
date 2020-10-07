from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class InstaUser(AbstractUser):
    following = models.ManyToManyField('self', symmetrical=False, default='self')
    display_name = models.CharField(max_length=20)
    photo = models.ImageField(upload_to='/static/', default='anonymous.jpg')

    def __str__(self):
        return f'@{self.username}'