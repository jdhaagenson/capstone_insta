from django.forms import ModelForm, Form
from .models import Post, Comment
from django import forms


class PostForm(ModelForm):
    caption = forms.CharField(widget=forms.Textarea)
    # author = forms.
    class Meta:
        model = Post
        fields = [
            'photo',
            'caption',
            'location',
            'author',
        ]
class SimplePostForm(forms.Form):
    photo = forms.ImageField(widget=forms.ClearableFileInput)
    caption = forms.CharField(widget=forms.Textarea)
    location = forms.CharField(max_length=50,required=False)

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = [
            'text',
        ]
