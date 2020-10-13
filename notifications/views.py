from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from notification.models import Notification
import copy
# Create your views here.


@login_required
def notification_view(request):
    notifications = Notification.objects.filter(alert_for=request.user.id)
    notifications_copy = copy.copy(notifications)
    Notification.objects.filter(alert_for=request.user.id).delete()
    return render(request, 'notification.html',{'notifications': notifications_copy})