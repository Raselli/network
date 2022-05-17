from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# class Post
    # Foreign key: User or Userprofile
    # fields: username (inh.: foreign key), content (text), likes (int, default=0), timestamp (daytime)

# class user profile
    # Foreign key: User
    # fields: username (inh.: foreign key), count: followers (int), count: following (int)
    # ? either: query for assosication list 'followers' & 'following' or save int on profile
        # for higher numbers: better, for this excercise: prob. overkill
    
# class like
    # foreign keys: post, users profile
    
# class follow
    # foreign keys: user profile (other), users profile (auth. user) OR user instead of u.profile