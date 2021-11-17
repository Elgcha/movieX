from django.db import models

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.IntegerField()
    known_for_department = models.CharField(max_length=100)
    also_known_as = models.JSONField()


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    release_date = models.DateField()
    # popularity
    poster_path = models.TextField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    original_title = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    genres = models.ManyToManyField(Genre, related_name='genre_movies')
    people = models.ManyToManyField(People, related_name='people_movies')

    def __str__(self):
        return self.title