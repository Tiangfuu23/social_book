# pylint: skip-file
from django.db import models
from django.contrib.auth import get_user_model
import uuid # Unique id purpose
from datetime import datetime
# Create your models here.
# DB for project

User = get_user_model() # User <- currently active user model –

# Define table profile
class Profile(models.Model): #inherited from models.Model
 user = models.ForeignKey(User ,on_delete=models.CASCADE) # Foreign key that link to current user model (User)
 id_user = models.IntegerField()
 bio = models.TextField(blank=True)
 profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
 coverimg = models.ImageField(upload_to='cover_images', default='cover-photo-black.jpg')
 location = models.CharField(max_length=100, blank=True)

 def __str__(self):
  return self.user.username # string representation of any object

class Post(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4) #Auto increasing id
  # callable object uuid.uuid4 -> Generate a random UUID.
  user = models.CharField(max_length = 100)
  data_type = models.IntegerField(default=1)
  image = models.ImageField(upload_to='post_images')
  video = models.FileField(upload_to='post_videos', null=True)
  caption = models.TextField()
  created_at = models.DateTimeField(default=datetime.now)
  no_of_likes = models.IntegerField(default = 0)

  def __str__(self):
   return self.user


class LikePost(models.Model):
 post_id = models.CharField(max_length=500)
 user_name = models.CharField(max_length=100)

 def __str__(self):
  return self.user_name
 
class FollowersCount(models.Model):
 follower = models.CharField(max_length=100)
 user = models.CharField(max_length=100)

 def __str__(self):
  return self.user

class Comment(models.Model):
 post = models.ForeignKey(Post, on_delete=models.CASCADE)
 profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
 comment = models.TextField()
 
#  id = models.AutoField(primary_key=True)
#  readonly_fields = ('id')
 def __str__(self):
  return self.profile.user.username