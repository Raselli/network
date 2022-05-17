from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User


def index(request):
    return render(request, "network/index.html")


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
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

# add ModelForm create_post

# def create_post
    # let user create new post

# def posts
    # load all posts from all users
    # descending based on timestamp: new -> old
    # post includes: username of creator, content, timestamp (mm/dd/yy, hh:mm), likes
    # Pagination:
        # render only 10 postsat once
        # next button for next 10 posts
        # back button for prev 10 posts
    # like/unlike button: JS, asynch., update like-count (no re-render)
    
# def user_profile
    # display: followers & following
    # display user's posts (reverse chronological order: newest -> oldest)
    # if visitor != user: follow/unfollow button
    
# def following
    # load all (recent?) posts of users the auth. user follows
    # login req.
    # ? merge with 'def posts' under same rendering with switchstatement/dict of different db queries ?
    # Pagination:
        # render only 10 postsat once
        # next button for next 10 posts
        # back button for prev 10 posts

# add ModelForm edit_post
  
# def edit_post
    # load textarea with posts content inside
    # save edited content with save button
        # save with JS: no re-render of page
    # check security: token, manipulation, get/post: check user_id
