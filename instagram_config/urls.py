"""instagram_config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from instauser.views import *
from post.views import *
from authentication.views import *


urlpatterns = [
    path('', PostFeedView.as_view(), name='homepage'),
    path('flt/', FollowPostView.as_view(), name='follow_feed'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('like/<int:postid>/', like_post, name='like'),
    path('dislike/<int:postid>', dislike_post, name='dislike'),
    path('signup/', CreateUser.as_view(), name='create_user'),
    path('follow/<int:userid>/', follow_user, name='follow'),
    path('unfollow/<int:userid>/', unfollow_user, name='unfollow'),
    path('user/<int:userid>/', ProfileView, name='profile'),
    path('post/<int:postid>/', PostDetailView, name='post_details'),
    path('post/', PostFormView.as_view(), name='create_post'),
    path('comlike/<int:commentid>/', like_comment),
    path('comdislike/<int:commentid>/', dislike_comment),
    # path('notifications/', ),
    path('admin/', admin.site.urls), ]
    
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

