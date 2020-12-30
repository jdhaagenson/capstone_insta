from django import forms
# from django.db.models import fields
from instauser.models import InstaUser, THEME_CHOICES


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = ['profile_pic', 'display_name', 'bio']


class ThemeForm(forms.Form):
    theme = forms.ChoiceField(choices=THEME_CHOICES)
