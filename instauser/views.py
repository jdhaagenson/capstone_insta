from django.shortcuts import render
from instauser.models import InstaUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Create your views here.
class IndexView(LoginRequiredMixin, TemplateView):

    def get(self, request):
        my_user = InstaUser.objects.filter(username=request.user.username).first()
        return render(request, "index.html", {"user": my_user})