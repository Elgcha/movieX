from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Movie, People, Genre

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'