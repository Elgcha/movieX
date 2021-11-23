from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail


# Create your models here.
class User(AbstractUser):
    email = models.EmailField() #blank=True
    #image_path = models.ImageField(blank=True, upload_to=users_image_path)
    image_path = ProcessedImageField(
        upload_to= './',
        blank = True,
        processors=[Thumbnail(200,300)],
        format='JPEG',
        options={'quality': 90},
    )


    # user가 상대편을 팔로우하면 follwings, 팔로우를 당하면 followers
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')