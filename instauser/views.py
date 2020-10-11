from django.shortcuts import render, HttpResponseRedirect, reverse
from instauser.models import InstaUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth import get_user
from post import models


# Create your views here.

@login_required
def follow_user(request, userid):
    to_follow = InstaUser.objects.get(pk=userid)
    user = InstaUser.objects.get(pk=request.user.id)
    user.followers.add(to_follow)
    user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def unfollow_user(request, userid):
    to_unfollow = InstaUser.objects.get(pk=userid)
    user = get_user(request)
    if to_unfollow in user.followers:
        user.followers.remove(to_unfollow)
        user.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class ProfileView(TemplateView):

    def get(self, request, user_id):
        profile = models.InstaUser.objects.get(id=user_id)
        posts = models.Post.objects.filter(insta_user=profile)
        user_following = profile.following.all()
        following_list = list(user_following)
        return render(request, 'profile.html', {'profile': profile, 'posts': posts, 'user_following': following_list})