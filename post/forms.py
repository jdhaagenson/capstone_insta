from django.forms import ModelForm, Form
from .models import Post, Comment


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = [
            'photo',
            'caption',
            'location',
            'author',
        ]


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
