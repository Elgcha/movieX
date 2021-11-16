from rest_framework import serializers
from rest_framework.utils import field_mapping
from .models import Article, Comment

class ArticleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Article
        fields = '__all__'



class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '_all__'
