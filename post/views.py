from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views import View
from django.views.generic import DetailView, CreateView, FormView, TemplateView, ListView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from django.contrib.auth import get_user


class PostFeedView(TemplateView):
    """Home page view"""
    template_name = "feed.html"

    @method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        user = get_user(request)
        posts = Post.objects.all()
        return render(request, self.template_name, {'user': user,
                                            'posts': posts
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
            form.save()
            return HttpResponseRedirect(reverse('homepage'))
        return render(request, self.template_name, {'form': form})


@login_required
def ProfileView(request, userid):
    user = InstaUser.objects.get(pk=userid)
    posts = Post.objects.filter(author_id=userid)
    return render(request, 'profile.html', {'user': user, 'posts': posts})


@login_required
def PostDetailView(request, postid):
    '''
    Posts comments on the post detail page
    '''
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form = form.cleaned_data
            Comment.objects.create(
                text=form.get('text'),
                creator=request.user,
                post=Post.objects.get(id=postid)
            )
            return HttpResponseRedirect(reverse('post_details'))
    form = CommentForm
    comments = Comment.objects.filter(post=postid)
    post = Post.objects.get(pk=postid)
    return render(request, 'details.html', {'post':post, 'form':form, 'comments':comments})


class FollowPostView(TemplateView):
    """Shows only the posts of people you are following, as well as your own."""
    @method_decorator(login_required)
    def get(self, request):
        user = InstaUser.objects.get(username=request.user)
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
    post.likes += 1
    post.save()
    return HttpResponseRedirect(reverse('post_details'))


@login_required
def dislike_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.dislikes += 1
    post.save()
    return HttpResponseRedirect(reverse('post_details'))


@login_required
def like_comment(request, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.likes += 1
    comment.save()
    return HttpResponseRedirect(reverse('post_details'))


@login_required
def dislike_comment(request, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.dislikes += 1
    comment.save()
    return HttpResponseRedirect(reverse('post_details'))
