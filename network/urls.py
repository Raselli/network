
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("edit", views.edit, name="edit"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("login", views.login_view, name="login"),
    path("following", views.index, name="following"),     
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),        
    path("profile/<str:profile_info>", views.index, name="profile")
]
