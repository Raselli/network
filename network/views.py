from http.client import OK
from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms

# TODO: check imports
from django.http import JsonResponse
import json

# TODO:
# models.py -> manytomany relationship: it is custom to use plural of my_like & following

 # merge profile + follow into index
 # thisway: only 1 pagination, new post on every page

from .models import User, Profile, Post

# Form: create post
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        
        widgets = {
            "content": forms.Textarea(attrs={"rows":3, "cols":10})
        }
        
        labels = {
            "content": "New Post"
        }


# Render all-posts, profile, following inside index
def index(request, profile_info=None):

    current_user = request.user

    if request.method == 'POST':

        form = PostForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.user_id = current_user.id
            form.save()
            return HttpResponseRedirect("/")
        else:
            # TODO: VALIDATION ERROR HANDLING
            return HttpResponseRedirect("/")     
            
    else:
        
        # TODO: handle if not logged in
        #@login_required(login_url='login')
        if "/following" in request.path:
            
            # Get PK-list of all users followed by current user
            current_users_profile = current_user.profile
            current_user_isfollowing = current_users_profile.following.all()
            other_users_pks = []
            for profile in current_user_isfollowing:
                other_users_pk = profile.user.id
                other_users_pks.append(other_users_pk)
            all_posts = Post.objects.select_related().filter(user_id__in=other_users_pks).order_by('-posted')
            

        elif "/profile" in request.path:
            other_user = get_object_or_404(User, username=profile_info)
            all_posts = Post.objects.filter(user=other_user.id).select_related().order_by('-posted')
            profile_info = Profile.objects.prefetch_related().get(user=other_user.id)
        # TODO: add information -> following or not -> follow_button.innerHTML?follow:unfollow @index.html

        else:
            all_posts = Post.objects.select_related().order_by('-posted')            

        # All posts liked by current_user
    # TODO: ? try / except necessairy ?      
        try:
            all_liked_posts = []
            my_likes = request.user.profile.my_like.all()
            for post in my_likes:
                all_liked_posts.append(post.id)
        except:
            all_liked_posts = None
            
        # TODO: handle if not logged in

        # Pagination
        paginate_posts = Paginator(all_posts, 10, orphans=0, allow_empty_first_page=True)
        page_number = request.GET.get('page')
        page_obj = paginate_posts.get_page(page_number)
        
        return render(request, "network/index.html" , {
            "form": PostForm(),            
            "profile": profile_info,
            "liked": all_liked_posts,
            "posts": page_obj
        })


# Receive request from follow.js
def follow(request):

    if request.method != "PUT":
        return JsonResponse({"message": "PUT request required."}, status=400)

    data = json.loads(request.body) # get profile name
    other_profile_name = data.get("other_profile_name") # how/where???
    users_profile = request.user.profile
    
    try:
        other_profile = Profile.objects.get(pk=other_profile_name.user_id)

    except:
        return JsonResponse({"message": "Profile not found."}, status=404)
    
    # Check for request manipulation 1
    if other_profile.user_id == request.user.id:
        return JsonResponse({"message": "It is not possible to (un)follow yourself."}, status=400)
    
    current_user_follows = users_profile.following.filter(from_profile_id=users_profile.id, to_profile_id=users_profile.id)

    # Follow
    if not current_user_follows:
        users_profile.following.add(other_profile)
        other_profile.followers += 1

    # Unfollow
    else:
        users_profile.following.remove(other_profile)
        other_profile.followers -= 1

    users_profile.save()
    other_profile.save()

    return JsonResponse({"message": f"Profile (un)followed."}, status=202)  


# Receive request from like.js
def like(request):
    
    if request.method != "PUT":
        return JsonResponse({"message": "PUT request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("id")
    users_profile = request.user.profile
    
    try:
        this_post = Post.objects.get(id=post_id)

    except:
        return JsonResponse({"message": f"Post #{post_id} not found."}, status=404)
    
    # Get all my_likes from db -> network_profile_my_like(s)
    users_likes = users_profile.my_like.all()

    if this_post not in users_likes:
        users_profile.my_like.add(post_id)
        this_post.likes += 1

    else:
        users_profile.my_like.remove(post_id)
        this_post.likes -= 1
    
    users_profile.save()
    this_post.save()

    return JsonResponse({"message": f"Post #{post_id} (un)liked."}, status=202)  


# Receive request from edit.js
def edit(request):
    
    if request.method != "PUT":
        return JsonResponse({"message": "PUT request required."}, status=400)

    data = json.loads(request.body)
    post_id = data.get("id")
    edited_content = data.get("content")

    try:
        this_post = Post.objects.get(id=post_id)

    except:
        return JsonResponse({"message": f"Post #{post_id} not found."}, status=404)
    
    if request.user.id != this_post.user_id:
# TODO: if wrong user: does not accept, but loads rejected content inside post
        return JsonResponse({"message": "Forbidden"}, status=403)

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
