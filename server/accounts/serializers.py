from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Profile
from movies.serializers import MovieSerializer

class UserSerializer(serializers.ModelSerializer):
    # 유저 정보를 받을 때 비밀번호를 알 수 없도록 write_only
    password = serializers.CharField(write_only=True)
    user_wants = MovieSerializer(many=True, read_only=True)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password', 'email', 'followings', 'followers', 'article_set', 'comment_set', 'image_path', 'user_wants',)

        # 유저등록시 작성할 필요가 없도록 read_only_fields
        read_only_fields = ('followings', 'followers', 'article_set', 'comment_set', 'image_path',) #want_movie, 프로필사진받아오기

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'
