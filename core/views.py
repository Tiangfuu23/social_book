# pylint: skip-file
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import Profile,Post, LikePost, FollowersCount, Comment
from django.contrib.auth.decorators import login_required
import random
# Create your views here.

@login_required(login_url='signin')
def index(request):
#  If else used for handle bug : Admin does not have profile record
 if Profile.objects.filter(user=request.user).first() != None:
  user_profile = Profile.objects.get(user=request.user) # Get profile of currently logged user

  user_following_list = []
  feed = []  # List of Posts which are owned/created by users in user_following_list

  user_following = FollowersCount.objects.filter(follower=request.user.username)

  for users in user_following:
    # Get username -> append to list
    user_following_list.append(users.user)


  for username in user_following_list:
    # Get posts
    feed_lists = Post.objects.filter(user=username)
    # Then append
    for post in feed_lists:
      feed.append(post) 

  # For get posts of current login user
  my_posts = Post.objects.filter(user=request.user.username)
  for post in my_posts:
    feed.append(post)


  ### USER SUGGESTION
  all_users = User.objects.all() 
  user_following_all = []

  for user in user_following:
    # Get user Object/Tuple/Record
    user_record = User.objects.get(username = user.user)
    user_following_all.append(user_record)

  new_suggestions_list = [x for x in list(all_users) if (x not in list(user_following_all))]
  # Remove current login user
  current_login_user = User.objects.get(username=request.user.username)
  new_suggestions_list.remove(current_login_user)
  
  # Random
  random.shuffle(new_suggestions_list)
 
  # Get suggestions_profile_list
  userId_list = []
  suggestions_profile_list = []

  for user in new_suggestions_list:
    userId_list.append(user.id)
  
  for ids in userId_list:
    # Careful with admin user
    if Profile.objects.filter(id_user=ids).first() != None:
      suggestions_profile_list.append(Profile.objects.get(id_user=ids))
  print(new_suggestions_list)

  ### Get All Comment objects
  comment_all = Comment.objects.all()

  return render(request, 'index.html', {'user_profile': user_profile, 'posts': feed, 'current_login_username': request.user.username, 'suggestions_profile_list': suggestions_profile_list[:4], 'comment_all': comment_all})
 else:
   return redirect('/signin')

# SIGNIN PAGE
def signin(request):
 if request.method == 'POST':
  username = request.POST['username']
  password = request.POST['password']

  user = auth.authenticate(username=username, password=password)
  if user is not None:
      auth.login(request, user) #Save user'id in session
      return redirect(index)
  else:
      messages.info(request, 'Username or Password is incorrect!')
      return redirect(signin)  
 else:
  return render(request, 'signin.html')
 
# SIGNUP PAGE
def signup(request):
 if request.method == 'POST':
  # print(request.POST)
  username = request.POST['username']
  email = request.POST['email']
  password = request.POST['password']
  password2 = request.POST['password2']
  if password == password2:
    if User.objects.filter(email = email).exists():
      # Email already exists
      messages.info(request, 'Email Taken')
      return redirect(signup)
    elif User.objects.filter(username = username).exists():
    # username already exists
      messages.info(request, 'Username Taken')
      return redirect(signup)
    else:
    #Can sign up new user
      user = User.objects.create_user(username=username, email=email, password=password) #create new user
      user.save() # save back to database

      #Log user in and redirect to setting pages
      user_login = auth.authenticate(username=username, password=password);
      auth.login(request, user_login);

      #create a profile object for the new user
      user_record = User.objects.get(username = username)
      new_profile = Profile.objects.create(user=user_record, id_user=user_record.id)
      new_profile.save()
      return redirect('settings')

  else:
   messages.info(request, 'Password Not Matching')
   return redirect(signup)
 else:
  return render(request, 'signup.html')

@login_required(login_url='signin')
def logout(request):
  auth.logout(request)
  return redirect(signin)

# Settings for account
@login_required(login_url='signin')
def settings(request):
  user_profile = Profile.objects.get(user=request.user) # Select user profile where user prop = current user login

  if request.method == 'POST':
    #Check whether user upload profile img or not 
    # if request.FILES.get('image') == None:
    #   image = user_profile.profileimg
    #   bio = request.POST['bio']
    #   location = request.POST['location']

    #   #Update user profile 
    #   user_profile.profileimg = image;
    #   user_profile.bio = bio
    #   user_profile.location = location
    #   user_profile.save()
    
    # if request.FILES.get('image') != None:
    #   image = request.FILES.get('image')
    #   bio = request.POST['bio']
    #   location = request.POST['location']

    #   #Update user profile 
      # user_profile.profileimg = image;
    #   user_profile.bio = bio
    #   user_profile.location = location
    #   user_profile.save()

    ### REFACTOR
    cover_image = request.FILES.get('cover_image')
    image = request.FILES.get('image') #Profile imgage
    user_profile.profileimg = image if(image != None) else user_profile.profileimg
    user_profile.coverimg = cover_image if(cover_image != None) else user_profile.coverimg
    user_profile.bio = request.POST['bio']
    user_profile.location = request.POST['location']
    user_profile.save()
    return redirect('/')
  else:
    return render(request, 'setting.html', {'user_profile': user_profile});

@login_required(login_url='signin')
def upload(request):
  if request.method == "POST":
    user = request.user.username
    image = request.FILES.get('image_upload')
    caption = request.POST['caption']
    
    new_post = Post.objects.create(user=user, image = image, caption = caption)
    new_post.save()

    print(new_post)
    return redirect('/')
  else:
    return redirect("/")

@login_required(login_url='signin')
def like_post(request):
  username = request.user.username
  post_id = request.GET.get('post_id') # get value of post_id query

  post = Post.objects.get(id = post_id)
  # Check current user liked post or not 
  like_filter = LikePost.objects.filter(post_id = post_id, user_name = username).first()

  if like_filter == None:
    new_like = LikePost.objects.create(post_id = post_id, user_name = username)
    new_like.save()

    post.no_of_likes = post.no_of_likes + 1
    post.save()

    return redirect('/#'+post_id)
  else:
    like_filter.delete()
    post.no_of_likes = post.no_of_likes - 1
    post.save()
    
    return redirect('/#'+post_id)

@login_required(login_url='signin')
def profile(request, username):
  user_object = User.objects.get(username=username) # User of profile page
  user_profile = Profile.objects.get(user=user_object) 
  user_posts = Post.objects.filter(user=username)
  user_posts_len = len(user_posts)

  # Check whether current login user had followed viewed_user or not
  current_login_user = request.user.username # ~ follower
  viewed_user = username

  if FollowersCount.objects.filter(follower=current_login_user, user=viewed_user).first() != None:
    btn_text = 'Unfollow'
  else:
    btn_text = 'Follow'

  # Get No.of followers of viewed_user
  user_followers = len(FollowersCount.objects.filter(user=username))

  # Get No.of following user of viewed_user
  user_following = len(FollowersCount.objects.filter(follower=username))

  context = {
    'user_object': user_object,
    'user_profile': user_profile,
    'user_posts': user_posts,
    'user_posts_len': user_posts_len,
    'btn_text': btn_text,
    'user_followers' : user_followers,
    'user_following' : user_following,
  }
  return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
  if request.method == "POST":
    follower = request.POST['follower'] 
    user = request.POST['user'] # viewed user

    # Query current login user had followed before ? 
    if FollowersCount.objects.filter(follower=follower, user=user).first() != None:
      # YES -> Delete follower
      delete_follower = FollowersCount.objects.get(follower=follower, user=user)
      delete_follower.delete()
      print("Delete succesfully")
      return redirect('/profile/'+user)
    else:
      #NO -> New follower
      new_follower = FollowersCount.objects.create(follower=follower, user=user)
      new_follower.save()
      print("Save successfully")
      return redirect('/profile/'+user)
  else:
    return redirect("/")


@login_required(login_url='signin')
def search(request):
  user_profile = Profile.objects.get(user=request.user)

  if request.method == "POST":
    searchedUserName = request.POST['username']
    # print(searchedUserName)
    username_object = User.objects.filter(username__icontains=searchedUserName) # Same as ilike in SQL
    # print(username_object)
    userId_profile = []
    profile_list = []

    for users in username_object:
      if(users.username != request.user.username):
        userId_profile.append(users.id)

    for ids in userId_profile:
      # profile_list.append(Profile.objects.get(id_user = ids))
      temp = Profile.objects.filter(id_user=ids)
      for profile in temp:
        profile_list.append(profile)

  return render(request,'search.html', {'user_profile': user_profile, 'current_login_username': request.user.username, 'username_profile_list': profile_list})

@login_required(login_url='signin')
def delete_post(request, id):
  deletePost = Post.objects.get(id = id)
  deletePost.delete()
  return redirect("/")

@login_required(login_url='signin')
def comment(request, post_id):
  if request.method == "POST":
    profile_object = Profile.objects.get(user=request.user)
    post_object = Post.objects.get(id=post_id)
    user_comment = request.POST.get('usercomment')
    new_comment = Comment.objects.create(profile=profile_object,post=post_object,comment=user_comment)
    new_comment.save()
  return redirect("/#"+str(post_id))