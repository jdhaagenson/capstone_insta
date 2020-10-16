from django.db import models
from instauser.models import InstaUser
from django.utils.timezone import now


# Create your models here.
class Notification(models.Model):
    message = models.CharField(max_length=140)
    alert_for = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    created_by = models.ForeignKey(InstaUser, on_delete=models.CASCADE, related_name='creator', default='')
    date = models.DateField(auto_now_add=True)
