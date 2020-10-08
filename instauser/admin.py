from django.contrib import admin
from instauser.models import InstaUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

admin.site.register(InstaUser, UserAdmin)