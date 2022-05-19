from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
# TODO: ? replace foreign key with oneToOneKey ?
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    followers = models.IntegerField(default=0)    
    following = models.ManyToManyField(
        "self", 
        blank=True,
        symmetrical=False,
        related_name="followings"
    )
    
    def __str__(self):
        return f"{self.user.username} follows {self.following} person(s) and has {self.followers} follower(s)" 

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    posted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
# TODO: liked -> asymmetrical? 
    liked = models.ManyToManyField(Profile, related_name="profiles")
    
    def __str__(self):
        return f"{self.user.username} posted on {self.posted}: {self.content}. {self.likes} like(s)." 
