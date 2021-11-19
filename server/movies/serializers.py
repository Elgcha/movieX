from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Movie, People, Genre, MovieComment

class MovieSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__' #영화 한줄평, 영화 좋아요, 
        read_only_fields = ('vote_count', 'vote_average', 'genres', 'people', 'want',)

class PeopleSerializer(serializers.ModelSerializer):

    class Meta:
        model = People
        fields = '__all__'
        read_only_fields = ('',)

class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = '__all__'

#영화 코멘트 모델만들기
class MovieCommentSerializer(serializers.ModelSerializer):
#유저가 영화평가한 개수 카운트하기
    class Meta:
        model = MovieComment
        fields= '__all__'
        read_only_fields = ('movie', 'user',)