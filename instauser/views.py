from django.shortcuts import render, HttpResponseRedirect, reverse
from instauser.models import InstaUser
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user
from post import models
from instauser.forms import EditProfileForm
from notifications.models import Notification


@login_required
def follow_user(request, userid):
    to_follow = InstaUser.objects.get(pk=userid)
    user = InstaUser.objects.get(pk=request.user.id)
    user.followers.add(to_follow)
    user.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def unfollow_user(request, userid):
    to_unfollow = InstaUser.objects.get(pk=userid)
    user = get_user(request)
    if to_unfollow in user.followers.all():
        user.followers.remove(to_unfollow)
        user.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))


@login_required
def ProfileView(request, userid):
    profile = InstaUser.objects.get(id=userid)
    posts = models.Post.objects.filter(author=profile.id)
    user_following = profile.followers.all()
    following_list = list(user_following)
    notifications = Notification.objects.filter(alert_for=profile)
    return render(
        request,
        "profile.html",
        {
            "profile": profile,
            "posts": posts,
            "user_following": following_list,
            "notifications": notifications,
        },
    )


@login_required
def edit_profile(request, userid):
    edit = InstaUser.objects.get(id=userid)
    if request.method == "POST":
        form = EditProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            edit.profile_pic = data["profile_pic"]
            edit.display_name = data["display_name"]
            edit.bio = data["bio"]
            edit.save()
        return HttpResponseRedirect(reverse("profile", args=[edit.id]))
    data = {
        "display_name": edit.display_name,
        "bio": edit.bio,
    }
    form = EditProfileForm(initial=data)
    return render(request, "edit.html", {"form": form})
