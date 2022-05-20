from queue import Empty
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required


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

def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid:
            form = form.save(commit=False)
            form.user_id = request.user.id
            form.save()
            return HttpResponseRedirect("/")
        else:
# TODO: VALIDATION ERROR HANDLING
            return HttpResponseRedirect("/")            
    else:
        return render(request, "network/index.html" , {
            "form": PostForm(),
            "posts": Post.objects.select_related().order_by('-posted')
        })
# TODO:
    # Pagination:
        # render only 10 postsat once
        # next button for next 10 posts
        # back button for prev 10 posts
    # like/unlike button: JS, asynch., update like-count (no re-render)
        
    # def user_profile
        # display: followers & following
        # display user's posts (reverse chronological order: newest -> oldest)
        # if visitor != user: follow/unfollow button

# Load others profiles
    # profile on seperate page or on same?  
def profile(request, profile_name):

    # Query profile
    other_user = get_object_or_404(User, username=profile_name)
    other_users_profile = Profile.objects.get(pk=other_user.id)

    # method == POST:
    if request.method == "POST":
        current_users_profile = request.user.profile
        
        # Check for request manipulation
        if other_user.id == request.user.id:
            return HttpResponseBadRequest('It is not possible to follow/unfollow yourself.')

        # Add/remove item from Profile.followings   
        if "follow" in request.POST:
            current_users_profile.following.add(other_users_profile)
            other_users_profile.followers += 1
# TODO: specific handlinmg for 'unfollow'
        else:
            current_users_profile.following.remove(other_users_profile)
            other_users_profile.followers -= 1     
        current_users_profile.save()
        other_users_profile.save()
        return HttpResponseRedirect(f"{profile_name}") 

    return render(request, "network/index.html" , {
        "profile": Profile.objects.prefetch_related().get(user=other_user.id),
        "posts": Post.objects.filter(user=other_user.id).select_related().order_by('-posted')
    })


# Posts of people the User follows
#TODO:
    # ? merge with 'def posts' under same rendering with switchstatement/dict of different db queries ?
@login_required(login_url='login')
def following(request):
    current_users_profile = request.user.profile
    current_user_isfollowing = current_users_profile.following.all()
    other_users_pks = []
    for profile in current_user_isfollowing:
        other_users_pk = profile.user.id
        other_users_pks.append(other_users_pk) 
    return render(request, "network/index.html" , {
        "posts": Post.objects.filter(pk__in=other_users_pks).select_related().order_by('-posted')
    })




#TODO:   
# Pagination:
    # render only 10 postsat once
    # next button for next 10 posts
    # back button for prev 10 posts

# edit post
    # modelForm
        # ? add ModelForm edit_post ?
        # or use jinja/JS
    
    # def edit_post
        # load textarea with posts content inside
        # save edited content with save button
            # save with JS: no re-render of page
        # check security: token, manipulation, get/post: check user_id






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

