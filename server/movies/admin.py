from django.contrib import admin
from .models import Movie, MovieComment, People, Genre

# Register your models here.
admin.site.register(Movie)
admin.site.register(People)
admin.site.register(Genre)
admin.site.register(MovieComment)


