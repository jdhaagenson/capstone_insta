from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, reverse
from .models import Post
from .forms import PostForm
from django.views import View
from django.views.generic import DetailView, CreateView, FormView, TemplateView, ListView, DeleteView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required


class PostFeedView(View):
    model = Post

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class PostFormView(CreateView):
    form_class = PostForm
    template_name = 'form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': 'form'})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            Post.objects.create(
                photo=data.get('photo'),
                caption=data.get('caption'),
                instauser=request.user,
                location=data.get('location')
            )
            return HttpResponseRedirect('/feed/')
        return render(request, self.template_name, {'form': form})


def PostsByUserView(request, userid):
    posts = Post.objects.filter(instauser_id=userid)
    return render(request, 'profile.html', {'posts': posts})


def PostDetailView(request, postid):
    post = Post.objects.get(pk=postid)
    return render(request, 'detail.html', {'post': post})


def PostsByFollowers(request):
    posts = Post.objects.filter(instauser_id=request.user.following)