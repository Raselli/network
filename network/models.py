from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    content = models.CharField(max_length=440)
    posted = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.username} posted on {self.posted}: {self.content}. {self.likes} like(s)." 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    followers = models.PositiveIntegerField(default=0)    
    following = models.ManyToManyField(
        "self", 
        blank=True,
        symmetrical=False,
        related_name="followings"
    )
    my_like = models.ManyToManyField(
        Post,
        blank=True,
        symmetrical=False,
        related_name="my_likes"
    )

    def __str__(self):
        return f"{self.user.username} follows {self.following.all().count()} person(s) and has {self.followers} follower(s)" 
