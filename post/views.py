from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Post, Comment, PostLikes
from notifications.models import Notification
from .forms import PostForm, CommentForm, SimplePostForm
from django.views.generic import CreateView, TemplateView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from django.contrib.auth import get_user
from django.urls import reverse_lazy
from helpers.helper_functions import get_tags
from django.http import JsonResponse
from instauser.forms import ThemeForm


def handler404View(request, exception, template_name="404.html"):
    response = render_to_response(template_name)
    return response


def handler500View(request):
    return render(request, '500.html', status=500)


def handler403View(request, exception):
    return render(request, '403.html')


class PostFeedView(TemplateView):
    """Home page view"""
    template_name = "feed.html"

    @method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        user = get_user(request)
        posts = Post.objects.all().order_by('-date')
        comments = Comment.objects.all()
        all_users = InstaUser.objects.all()
        return render(request, self.template_name, {'user': user,
                                                    'posts': posts,
                                                    'comments': comments,
                                                    'all_users': all_users,
        })


class PostFormView(CreateView):
    """Create a new post"""
    form_class = PostForm
    template_name = 'upload.html'

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            caption = form.cleaned_data.get('caption')
            form.save()
            if get_tags(caption) is not None:
                for alerted_username in get_tags(caption):
                    new_notification=Notification.objects.create(
                        message=caption,
                        alert_for=InstaUser.objects.get(username=alerted_username),
                        created_by=request.user
                    )
            return HttpResponseRedirect(reverse('homepage'))
        return render(request, self.template_name, {'form': form})


def simple_form_view(request):
    if request.method == 'POST':
        form = SimplePostForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                author=request.user,
                location=data.get('location'),
                caption=data.get('caption'),
                photo=data.get('photo')
            )
            caption = data.get('caption')
            if get_tags(caption) is not None:
                for alerted_username in get_tags(caption):
                    Notification.objects.create(
                        message=caption,
                        alert_for=InstaUser.objects.get(username=alerted_username),
                        created_by=request.user
                    )
            # form.save()
            return HttpResponseRedirect(reverse('homepage'))
    form = SimplePostForm()
    return render(request, 'upload.html', {'form': form})



@login_required
def PostDetailView(request, postid):
    '''
    Posts comments on the post detail page
    '''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            new_comment = Comment.objects.create(
                text=form.get('text'),
                creator=request.user,
                post=Post.objects.get(id=postid)
            )
            if get_tags(new_comment.text) is not None:
                for alerted_username in get_tags(new_comment.text):
                    new_notification = Notification.objects.create(
                        message = new_comment.text,
                        alert_for = InstaUser.objects.get(username=alerted_username),
                        created_by = request.user
                    )
            return HttpResponseRedirect(request.META.get('HTTP_REFERER','post_details'))
    form = CommentForm
    comments = Comment.objects.filter(post=postid)
    post = Post.objects.get(pk=postid)
    return render(request, 'details.html', {'post':post, 'form':form, 'comments':comments})


class FollowPostView(TemplateView):
    """Shows only the posts of people you are following, as well as your own."""
    @method_decorator(login_required)
    def get(self, request):
        user = get_user(request)
        followers = user.followers.all()
        posts = Post.objects.filter(author__in=followers)
        my_posts = Post.objects.filter(author=user).values()
        posts = posts.union(my_posts).order_by('-date')
        return render(request, 'feed.html', {'user': user,
                                             'posts': posts}
                      )


@login_required
def like_post(request, postid):
    post = Post.objects.get(pk=postid)
    user = get_user(request)
    if PostLikes.objects.get_or_create(post_id=postid, user=user):
        liked = PostLikes.objects.get(post=post, user=user)
        if liked.liked:
            post.likes -= 1
            liked.liked = False
            post.save()
            liked.save()
        else:
            post.likes += 1
            liked.liked = True
            post.save()
            liked.save()
    else:
        tolike = PostLikes.objects.create(post=post, user=user)
        tolike.liked = True
        post.likes += 1
        post.save()
        tolike.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','homepage'))


@login_required
def dislike_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.dislikes += 1
    post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','homepage'))

@login_required
def delete_all_comments(request, postid):
    this_post = Post.objects.get(id=postid)
    comments = Comment.objects.filter(post__id=this_post.id).delete()
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def delete_comment(request, commentid):
    comment = Comment.objects.get(id=commentid).delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','homepage'))


@login_required
def like_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.likes += 1
    comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','post_details'))


@login_required
def dislike_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.dislikes += 1
    comment.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER','post_details'))


@login_required
def delete_post(request, postid):
    Post.objects.get(id=postid).delete()
    return HttpResponseRedirect(reverse('homepage'))


def permanent_theme_change(request, userid):
    user = InstaUser.objects.get(userid)
    if request.method == 'POST':
        form = ThemeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user.theme = data.get('theme')
            return HttpResponseRedirect(reverse('profile'))
    form = ThemeForm()
    return render(request, 'edit.html', {'user': user, 'form': form, })


# TODO: FINISH PERMANENT THEME CHANGE FUNCTION VIEW
# TODO: GET RID OF THE LINES ON THE EDGES OF THE FEED, DONT NEED WITH SEAMLESS BACKGROUNDS
