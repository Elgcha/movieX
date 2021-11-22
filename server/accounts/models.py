from django.core import validators
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import Model
from imagekit.models import ProcessedImageField
from imagekit.processors import Thumbnail

#def users_image_path(instance, filename):
    # MEDIA_ROOT/user_<pk>/경로로 <filename> 이름으로 업로드
    #return f'user_{instance.profile_pk}/{filename}'


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

class Profile(models.Model):
        image_path = ProcessedImageField(
        upload_to = './',
        blank = True,
        processors=[Thumbnail(200,300)],
        format='JPEG',
        options={'quality': 90},
    )

