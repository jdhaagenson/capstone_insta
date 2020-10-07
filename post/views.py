from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Post
from .forms import PostForm
from django.views import View
from django.views.generic import FeedView, TemplateView, ListView, DeleteView


class FeedView(FeedView):
    model = Post


class PostFormView(View):
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

