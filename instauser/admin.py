from django.contrib import admin
from instauser.models import InstaUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.

UserAdmin.fieldsets += ('Custom fields set', {'fields': ('display_name', 'followers')}),

admin.site.register(InstaUser, UserAdmin)