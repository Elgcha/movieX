from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.utils import field_mapping

from .models import Movie, People, Genre, MovieComment, MovieSite

class GenreSerializer(serializers.ModelSerializer):
   # name = Genre.objects.filter()

    class Meta:
        model = Genre
        fields = '__all__'

class PeopleSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        genres = GenreSerializer(many=True, read_only=True)
        class Meta:
            model = Movie
            fields = ('title', 'genres','id','poster_path')

    movie_title = MovieSerializer(source='people_movies', many=True)

    class Meta:
        model = People
        fields = '__all__'
        # read_only_fields = ('',)

#영화 코멘트 모델만들기
class MovieCommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()

# pk말고 이름을 명시할 수 있도록
    def get_username(self, obj):
        return obj.user.username

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('image_path',)
        
    user_image = UserSerializer(source='user', read_only='True') 

    class Meta:
        model = MovieComment
        fields= '__all__'
        read_only_fields = ('movie', 'user',)

class MovieSerializer(serializers.ModelSerializer):
    class PeopleSerializer(serializers.ModelSerializer):
        class Meta:
            model = People
            fields = ('id', 'name', 'birthday', 'profile_path', 'also_known_as', 'known_for_department',)
            read_only_fields = ('',)

    genres = GenreSerializer(many=True, read_only=True)
    people = PeopleSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = '__all__' #영화 한줄평, 영화 좋아요, 
        read_only_fields = ('vote_count', 'vote_average', 'people', 'want','genres',)





### 인물의 출연영화
class PeopleMovieListSerializer(serializers.ModelSerializer):
    class MovieSerializer(serializers.ModelSerializer):
        genres = GenreSerializer( many=True, read_only=True)
        class Meta:
            model = Movie
            fields = ('id', 'genres', 'title', 'runtime', 'poster_path', 'release_date', 'vote_average',)

    movie_title = MovieSerializer(source='people_movies', many=True)

    class Meta:
        model = People
        fields = ('name', 'movie_title',)

class MovieSiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieSite
        fields = '__all__'
        read_only_fields = ('movie', 'user',)