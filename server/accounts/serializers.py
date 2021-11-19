from django.db import models
from rest_framework import serializers
from django.contrib.auth import get_user_model

from movies.models import Movie

from .models import Profile

from movies.serializers import MovieSerializer, MovieCommentSerializer


class UserSerializer(serializers.ModelSerializer):
    # 유저 정보를 받을 때 비밀번호를 알 수 없도록 write_only
    # class MoviedetailSerializer(serializers.ModelSerializer):
    #     model = Movie
    #     fields = ('genres', 'title', '')
    password = serializers.CharField(write_only=True)

    user_wants = MovieSerializer(many=True, read_only=True) #객체로 가져오게해줌
    rated_movie= MovieCommentSerializer(many=True, read_only=True)


    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'followings', 'followers', 'article_set', 'comment_set', 'image_path', 'user_wants', 'rated_movie',)

        # 유저등록시 작성할 필요가 없도록 read_only_fields

        read_only_fields = ('followings', 'followers', 'article_set', 'comment_set',) #want_movie, 프로필사진받아오기


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
