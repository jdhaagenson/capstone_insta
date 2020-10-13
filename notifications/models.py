from django.db import models
from instauser.models import InstaUser

# Create your models here.
class Notification(models.Model):
    message = models.CharField(max_length=140)
    alert_for = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    created_by = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='creator', default='')