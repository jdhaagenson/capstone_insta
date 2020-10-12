from django import forms
# from django.db.models import fields
from instauser.models import InstaUser


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = InstaUser
        fields = ['profile_pic', 'display_name', 'bio']