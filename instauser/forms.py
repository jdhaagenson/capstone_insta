from django import forms
from .models import InstaUser


class LoginForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = [
            'display_name',
            'username',
            'password',
            'photo'
        ]