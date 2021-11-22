from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Article
        fields = ('id', 'username', 'user', 'title', 'content', 'created_at', 'updated_at',)
        read_only_fields = ('user',)

class CommentSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    def get_username(self, obj):
        return obj.user.username

    class Meta:
        model = Comment
        fields = ('id', 'username', 'user', 'content', 'created_at', 'updated_at', 'article',)
        read_only_fields = ('user', 'article',)
