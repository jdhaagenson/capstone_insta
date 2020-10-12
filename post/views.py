from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.views import View
from django.views.generic import DetailView, CreateView, FormView, TemplateView, ListView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from instauser.models import InstaUser
from django.contrib.auth import get_user
from django.urls import reverse_lazy


class PostFeedView(TemplateView):
    """Home page view"""
    template_name = "feed.html"

    @method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        user = get_user(request)
        posts = Post.objects.all()
        comments = Comment.objects.all()
        return render(request, self.template_name, {'user': user,
                                                    'posts': posts,
                                                    'comments': comments,
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
    post.likes += 1
    post.save()
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def dislike_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.dislikes += 1
    post.save()
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def like_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.likes += 1
    comment.save()
    return HttpResponseRedirect(reverse('post_details'))


@login_required
def dislike_comment(request, postid, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.dislikes += 1
    comment.save()
    return HttpResponseRedirect(reverse('post_details'))


class PostDetails(DetailView):
    form_class = CommentForm
    template_name = 'details.html'

    def get(self, request, postid, *args, **kwargs):
        post = Post.objects.get(pk=postid)
        comments = Comment.objects.filter(post_id=postid)
        user = get_user(request)
        form = CommentForm()
        return render(request, 'details.html', {'form':form, 'user':user, 'post':post, 'comments':comments})

    def post(self, request, postid, *args, **kwargs):
        form = CommentForm(request.POST)
        user = get_user(request)
        post = Post.objects.get(pk=postid)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                text=data.get('text'),
                post=post,
                creator=user)
            return reverse_lazy('post_details')


class PostDelete(DeleteView):
    model = Post
    success_url = reverse_lazy('homepage')


