from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    likes = models.IntegerField(default=0)
    posted = models.DateTimeField(auto_now_add=True)
     
    def __str__(self):
        return f"{self.username} posted on {self.posted}: \"{self.content}\". [{self.likes} like(s)]" 

class Profile(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)
    following = ArrayField(models.IntegerField(unique=True))
    liked = ArrayField(models.IntegerField(unique=True))   
    # ? either: query for assosication list 'followers' & 'following' or save int on profile

    def __str__(self):
        return f"{self.user.username} has {self.followers} follower(s) and follows {self.following}" 
