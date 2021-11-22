from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinLengthValidator, MinValueValidator

# Create your models here.
class Genre(models.Model): 
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=100)
    popularity = models.FloatField(validators=[MinValueValidator(0)])
    profile_path = models.TextField()
    adult = models.BooleanField()
    gender = models.IntegerField()
    tmdb_id = models.IntegerField()
    also_known_as = models.JSONField(null=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField(validators=[MinValueValidator(0)])
    poster_path = models.TextField()
    vote_count = models.IntegerField(validators=[MinValueValidator(0)])
    vote_average = models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(10)])
    adult = models.BooleanField()
    original_title = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre, related_name='genre_movies')
    people = models.ManyToManyField(People, related_name='people_movies')
    tmdb_id = models.IntegerField()
    overview = models.TextField()
    want = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='user_wants')

    def __str__(self):
        return self.title

# tmdb 아이디를 통해서 고유 id값을 받아오고, 그 것을 이용해서 연결해 준다.
#영화 코멘트 모델만들기

class MovieComment(models.Model): # 유저하나가 영화 하나만 평가할수있도록 생각
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=200, validators=[MinLengthValidator(0)], blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    rate = models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(10)])

    def __str__(self):
        return self.content
