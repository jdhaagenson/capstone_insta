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
    template_name = "feed.html"

    @method_decorator(login_required)
    def get(self,request, *args, **kwargs):
        user = get_user(request)
        posts = Post.objects.all()
        return render(request, self.template_name, {'user': user,
                                            'posts': posts
        })


class PostFormView(CreateView):
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
            data = form.cleaned_data
            # Post.objects.create(
            #     photo=data.get('photo'),
            #     caption=data.get('caption'),
            #     author=data.get('author'),
            #     location=data.get('location')
            # )
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
    comments = Comment.objects.all()
    post = Post.objects.get(pk=postid)
    return render(request, 'details.html', {'post':post, 'form':form, 'comments':comments})


@login_required
def FollowPostView(request):
    user = InstaUser.objects.get(username=request.user)
    followers = user.followers.all()
    posts = Post.objects.filter(author__in=followers)
    my_posts = Post.objects.filter(author=user).values()
    posts = posts.union(my_posts).order_by('-date')
    return render(request, 'feed.html', {'user': user,
                                         'posts': posts
    })


def like_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.likes += 1
    post.save()
    return HttpResponseRedirect(reverse('post_details'))


def dislike_post(request, postid):
    post = Post.objects.get(pk=postid)
    post.dislikes += 1
    post.save()
    return HttpResponseRedirect(reverse('post_details'))


def like_comment(request, commentid):
    comment = Comment.objects.get(pk=commentid)
    comment.likes += 1
    comment.save()
    return HttpResponseRedirect(reverse('post_details'))


class PostCommentView(DetailView):
    """
    Post comments with class view
    """
    form_class = CommentForm
    template_name = 'details.html'

    @method_decorator(login_required)
    def get(self, request, postid):
        post = Post.objects.get(pk=postid)
        form = self.form_class()
        comments = Comment.objects.filter(post=postid)
        return render(request, self.template_name, {'form': form,
                                                    'post': post,
                                                    'comments': comments})

    @method_decorator(login_required)
    def post(self, request, postid):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Comment.objects.create(
                post=Post.objects.get(pk=postid),
                creator=request.user,
                text=data.get('text')
            )