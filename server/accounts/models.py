from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    email = models.EmailField()


    # user가 상대편을 팔로우하면 follwings, 팔로우를 당하면 followers
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

