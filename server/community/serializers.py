from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Article, Comment
from accounts.serializers import UserSerializer

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username
    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ('image_path',)
        
    user_image = UserSerializer(source='user', read_only='True') 


    class Meta:
        model = Article
        fields = ('id', 'username', 'user', 'title', 'content', 'created_at', 'updated_at','views_num', 'user_image',)
        read_only_fields = ('user',)


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ('id', 'username', 'user', 'content', 'created_at', 'updated_at', 'article',)
        read_only_fields = ('user', 'article',)
