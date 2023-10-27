# pylint: skip-file
from django.urls import path
from . import views
import uuid
urlpatterns = [
 path('', views.index, name="index"),
 path('upload', views.upload, name="upload"),
 path('like-post', views.like_post, name="like-post"),
 path('delete-post/<uuid:id>', views.delete_post, name="like-post"),
 path('follow', views.follow, name="follow"),
 path('search', views.search, name="search"),
 path('profile/<str:username>', views.profile, name="profile"), #expect a (username) arg of type string
 path('signup', views.signup, name='signup'),
 path('signin', views.signin, name='signin'),
 path('logout', views.logout, name='logout'),
 path('settings', views.settings, name='settings'),
 path('comment/<uuid:post_id>', views.comment, name='comment'),
]