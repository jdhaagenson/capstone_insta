from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post, Comment, SharePost
from notifications.models import Notification
from .forms import PostForm, CommentForm, ShareForm
from django.views import View
from django.views.generic import (
    DetailView,
    CreateView,
    FormView,
    TemplateView,
    ListView,
    DeleteView,
)
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from django.contrib.auth import get_user
from django.urls import reverse_lazy
from helpers.helper_functions import get_tags
from itertools import chain


class PostFeedView(TemplateView):
    """Home page view"""

    template_name = "feed.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        user = get_user(request)
        posts = chain(
            Post.objects.all().order_by("-date"),
            SharePost.objects.all().order_by("-date"),
        )

        comments = Comment.objects.all()
        return render(
            request,
            self.template_name,
            {
                "user": user,
                "posts": posts,
                "comments": comments,
            },
        )


class PostFormView(CreateView):
    """Create a new post"""

    form_class = PostForm
    template_name = "upload.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {"form": form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data.get("caption")
            form.save()
            if get_tags(caption) is not None:
                for alerted_username in get_tags(caption):
                    new_notification = Notification.objects.create(
                        message=caption,
                        alert_for=InstaUser.objects.get(username=alerted_username),
                        created_by=request.user,
                    )
            return HttpResponseRedirect(reverse("homepage"))
        return render(request, self.template_name, {"form": form})


@login_required
def SharePostView(request, postid):
    """Shares a post"""
    shared_post = Post.objects.filter(id=postid)
    form = ShareForm()
    if request.method == "POST":
        form = ShareForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            new_post = SharePost.objects.create(
                post=Post.objects.filter(id=postid).first(),
                caption=data.get("caption"),
                author=request.user,
            )
        return HttpResponseRedirect(reverse("homepage"))
    return render(request, "share.html", {"form": form, "shared_post": shared_post})


@login_required
def PostDetailView(request, postid):
    """
    Posts comments on the post detail page
    """
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            new_comment = Comment.objects.create(
                text=form.get("text"),
                creator=request.user,
                post=Post.objects.get(id=postid),
            )
            if get_tags(new_comment.text) is not None:
                for alerted_username in get_tags(new_comment.text):
                    new_notification = Notification.objects.create(
                        message=new_comment.text,
                        alert_for=InstaUser.objects.get(username=alerted_username),
                        created_by=request.user,
                    )
            return HttpResponseRedirect(
                request.META.get("HTTP_REFERER", "post_details")
            )
    form = CommentForm
    comments = Comment.objects.filter(post=postid)
    post = Post.objects.get(pk=postid)
    return render(
        request, "details.html", {"post": post, "form": form, "comments": comments}
    )


class FollowPostView(TemplateView):
    """Shows only the posts of people you are following, as well as your own."""

    @method_decorator(login_required)
    def get(self, request):
        user = get_user(request)
        followers = user.followers.all()
        posts = Post.objects.filter(author__in=followers)
        my_posts = Post.objects.filter(author=user).values()
        posts = posts.union(my_posts).order_by("-date")
        return render(request, "feed.html", {"user": user, "posts": posts})


@login_required
def like_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "homepage"))


@login_required
def dislike_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.dislikes += 1
    post.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "homepage"))


@login_required
def delete_all_comments(request, postid):
    this_post = Post.objects.get(id=postid)
    comments = Comment.objects.filter(post__id=this_post.id).delete()
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def delete_comment(request, commentid):
    comment = Comment.objects.get(id=commentid).delete()
    return HttpResponseRedirect(reverse("homepage"))


@login_required
def like_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.likes += 1
    comment.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "post_details"))


@login_required
def dislike_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.dislikes += 1
    comment.save()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "post_details"))


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy("homepage")
