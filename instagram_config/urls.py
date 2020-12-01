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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from instauser.views import *
from post.views import *
from authentication.views import *
from notifications.views import *
from django.conf.urls import url
from django.views.static import serve



urlpatterns = [
    path('', PostFeedView.as_view(), name='homepage'),
    path('flt/', FollowPostView.as_view(), name='follow_feed'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('signup/', CreateUser.as_view(), name='create_user'),
    path('deleteallcomments/<int:postid>/', delete_all_comments, name='delete_post_comments'),
    path('deletecomment/<int:commentid>/', delete_comment, name='delete_specific_comment'),
    path('post/<int:postid>/like/', like_post, name='like'),
    path('post/<int:postid>/dislike/', dislike_post, name='dislike'),
    path('post/<int:postid>/<int:commentid>/like/', like_comment, name="like_comment"),
    path('post/<int:postid>/<int:commentid>/dislike/', dislike_comment, name="dislike_comment"),
    path('post/<int:postid>/', PostDetailView, name='post_details'),
    # path('post/', PostFormView.as_view(), name='create_post'),
    path('post/', simple_form_view, name='create_post'),
    path('user/<int:userid>/unfollow/', unfollow_user, name='unfollow'),
    path('user/<int:userid>/follow/', follow_user, name='follow'),
    path('user/<int:user_id>/', ProfileView, name='profile'),
    path('user/<int:user_id>/edit/', edit_profile, name='editprofile'),
    path('deletepost/<int:postid>/', delete_post, name="deletepost"),
    path('notifications/', notification_view, name='notifications'),
    path('admin/', admin.site.urls),
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'post.views.handler404View'
handler403 = 'post.views.handler403View'
handler500 = 'post.views.handler500View'