from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.urls import reverse
from django import forms
from django.http import JsonResponse
import json


# TODO:
# models.py -> manytomany relationship: it is custom to use plural of my_like & following
# javascript: asynch. improve edit-response.

from .models import User, Profile, Post

# Form: create post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 5, 
                "class": "new_post_textarea",
                "placeholder": "Enter your message (Maximum of 440 characters)."
            })
        }
        
        labels = {
            "content": "New Post"
        }
        
    def clean(self):
        super(PostForm, self).clean()
        content = self.cleaned_data.get('content')
        
        # Check for whitespace-only or empty content
        if content == None or content.isspace() == True:
            msg = 'Content can\'t be empty.'
            self.add_error('content', msg)
        
        # Check if content too long
        elif len(content) > 440:
            msg = 'Post can\'t be longer than 440 characters.'
            self.add_error('content', msg)

        return self.cleaned_data


# Render all-posts, profile, following inside index
def index(request, profile_info=None):
    current_user = request.user
    form = PostForm()   
    
    # New post
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit = False)
            post.user_id = current_user.id
            post.save() 
            return redirect('/')

    # All posts made by users followed by the current user
    if "/following" in request.path:
        
        # Check for authentication
        if not request.user.is_authenticated:
            return render(request, "network/login.html")
        
        # Get PK-list of all users followed by current user
        current_user_isfollowing = current_user.profile.following.all()            
        other_users_pks = []
        for profile in current_user_isfollowing:
            other_users_pk = profile.user.id
            other_users_pks.append(other_users_pk)
        
        # All posts of all users followed by current user
        all_posts = Post.objects.select_related().filter(user_id__in=other_users_pks).order_by('-posted')
        
    # Specific user’s profile page & posts
    elif "/profile" in request.path:
        other_user = get_object_or_404(User, username=profile_info)            
        following = "Follow"          
        
        # Information: profile followed or not
        if request.user.is_authenticated:
            followings = request.user.profile.following.all()
            for profile in followings:
                following = "Unfollow" if (profile.id == other_user.id) else "Follow"
                
        # All posts from specific profile                 
        all_posts = Post.objects.filter(user=other_user.id).select_related().order_by('-posted')
        profile_info = [Profile.objects.prefetch_related().get(user=other_user.id), following]

    # Load all posts: No constraints
    else:
        all_posts = Post.objects.select_related().order_by('-posted')            

    # All posts liked by current_user
    all_liked_posts = []
    if request.user.is_authenticated:
        my_likes = request.user.profile.my_like.all()
        for post in my_likes:
            all_liked_posts.append(post.id)

    # Pagination
    paginate_posts = Paginator(all_posts, 10, orphans=0, allow_empty_first_page=True)
    page_number = request.GET.get('page')
    page_obj = paginate_posts.get_page(page_number)
    return render(request, "network/index.html" , {
        "form": form,
        "profile": profile_info,
        "liked": all_liked_posts,
        "posts": page_obj
    })


# Follow|Unfollow profile. Request from buttonevents.js.
@login_required
def follow(request):

    # Method = PUT only
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Fetch data
    data = json.loads(request.body)
    other_profile_name = data.get("other_profile_name")
    users_profile = request.user.profile

    # Query for Profile to follow
    try:
        other_user = User.objects.get(username=other_profile_name)
    except:
        return JsonResponse({"error": "Profile not found."}, status=404)
    other_profile = Profile.objects.prefetch_related().get(user=other_user.id)

    # Check for request manipulation: follow-self
    if other_profile.user_id == request.user.id:
        return JsonResponse({"error": "It is not possible to (un)follow yourself."}, status=400)
    
    # Follow: Add/remove to/from Profile.followings & Profile.followers
    current_user_followings = Profile.objects.filter(following__id=other_profile.user_id)    
    if current_user_followings.exists():
        users_profile.following.remove(other_profile.user_id)
        other_profile.followers -= 1
    else:
        users_profile.following.add(other_profile.user_id)
        other_profile.followers += 1

    # Commit changes
    users_profile.save()
    other_profile.save()
    return JsonResponse({"message": "Profile (un)followed."}, status=202)  


# Like|Unlike post. Request from buttonevents.js.
@login_required
def like(request):
    
    # Method = PUT only
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Fetch data
    data = json.loads(request.body)
    post_id = data.get("id")
    users_profile = request.user.profile
    
    # Query for post
    try:
        this_post = Post.objects.get(id=post_id)
    except:
        return JsonResponse({"error": f"Post #{post_id} not found."}, status=404)
    
    # Get all my_likes from db network_profile_my_like(s)
    users_likes = users_profile.my_like.all()
    
    # Add/remove like
    if this_post not in users_likes:
        users_profile.my_like.add(post_id)
        this_post.likes += 1
    else:
        users_profile.my_like.remove(post_id)
        this_post.likes -= 1
    
    # Commit changes
    users_profile.save()
    this_post.save()
    return JsonResponse({"message": f"Post #{post_id} (un)liked."}, status=202)  


# Edit post. Request from buttonevents.js.
@login_required
def edit(request):
    
    # Method = PUT only
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    # Fetch data
    data = json.loads(request.body)
    post_id = data.get("id")
    edited_content = data.get("content")

    # Check for valid data
    if edited_content == '':
        return JsonResponse({"error": f"Content can\'t be empty."}, status=400)
    if edited_content.isspace() == True:
        return JsonResponse({"error": f"Only whitespace not allowed."}, status=400)
    if len(edited_content) < 1:
        return JsonResponse({"error": f"Content too short: Minimum length of 1 character."}, status=400)
    if len(edited_content) > 440:
        return JsonResponse({"error": f"Content too long: Maximum length of 440 characters."}, status=400)
  
    # Query for post
    try:
        this_post = Post.objects.get(id=post_id)
    except:
        return JsonResponse({"error": f"Post #{post_id} not found."}, status=404)
    
    # Check for post ownership
    if request.user.id != this_post.user_id:
        return JsonResponse({"error": "Forbidden"}, status=403)

    # Commit changes
    this_post.content = edited_content
    this_post.save()
    return JsonResponse({"message": f"Post #{post_id} edited."}, status=202)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
            
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            
            # Create profile
            profile = Profile.objects.create(user=user)
            profile.save()
            
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
