from rest_framework import serializers
from django.contrib.auth import get_user_model
from movies.models import Movie, MovieComment
from movies.serializers import MovieSerializer, MovieCommentSerializer, GenreSerializer


class UserSerializer(serializers.ModelSerializer):
    # 유저 정보를 받을 때 비밀번호를 알 수 없도록 write_only
    password = serializers.CharField(write_only=True)
    user_wants = MovieSerializer(many=True, read_only=True) #객체로 가져오게해줌
    
    #필드에 없으니 필수로입력하지않아도되네(signup)
    class Meta:
        model = get_user_model()
        #fields = ('__all__')
        fields = ('username', 'password', 'email', 'followings', 'followers', 'article_set', 'comment_set', 'image_path', 'user_wants',)

        # 유저등록시 작성할 필요가 없도록 read_only_fields
        read_only_fields = ('followings', 'followers', 'article_set', 'comment_set',)


class MovieCommentListSerializer(serializers.ModelSerializer):

    class MovieCommentSerializer(serializers.ModelSerializer):
        username = serializers.SerializerMethodField()
        title = serializers.SerializerMethodField()
        # pk말고 이름을 명시할 수 있도록
        def get_username(self, obj):
            return obj.user.username
        def get_title(self, obj):
            return obj.movie.title
        class Meta:
            model = MovieComment
            fields = ('id', 'username','title', 'content', 'rate','created_at', 'updated_at', )

    moviecomment_set_name = MovieCommentSerializer(source='moviecomment_set', many=True,)
    class Meta:
        model = get_user_model()
        fields = ('moviecomment_set', 'moviecomment_set_name')


class RecommendSerializer(serializers.ModelSerializer):

    class MovieCommentSerializer(serializers.ModelSerializer):

        class MovieSerializer(serializers.ModelSerializer):
            genres = GenreSerializer(many=True, read_only=True)
            class Meta:
                model = Movie
                fields = ('genres', 'tmdb_id', 'title', 'popularity', 'vote_count', 'vote_average', )
        
        title = serializers.SerializerMethodField()
        movie = MovieSerializer() #many=True가 아니였음
        # pk말고 이름을 명시할 수 있도록
        def get_title(self, obj):
            return obj.movie.title
        class Meta:
            model = MovieComment
            fields = ('title', 'rate', 'movie', )

    moviecomment_set_name = MovieCommentSerializer(source='moviecomment_set', many=True,)
    class Meta:
        model = get_user_model()
        fields = ('moviecomment_set_name',)
