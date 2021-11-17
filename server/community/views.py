from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
#from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from .models import Article, Comment
from .serializers import ArticleSerializer, CommentSerializer

# Create your views here.

@api_view(['GET'])
def community(request):
    if request.method == 'GET':
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

@api_view(['POST'])
def create(request):
    serializer = ArticleSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#게시글 상세조회, 수정, 삭제
@api_view(['GET', 'PUT', 'DELETE'])
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    

    if request.method == 'GET':  #게시글 조회
        serializer = ArticleSerializer(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT': #게시글 수정
        serializer= ArticleSerializer(article, data= request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE': #게시글 삭제
        article.delete()
        data = {
            'message': '글이 삭제 되었습니다.',
        }
        return Response(data, status.HTTP_204_NO_CONTENT)
        
def update(request):
    pass

def delete(request):
    pass

@api_view(['POST'])
def comment_create(request, article_pk):
    article = get_object_or_404(Article, pk = article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, article=article)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def comment_detail(request):
    pass

@api_view(['PUT', 'DELETE'])
def comment_update(request, article_pk, comment_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment = article.comment_set.get(pk=comment_pk)

    #if not request.user.articles.filter(pk=article_pk).exist():
    #    return Response({'message': '권한이 없습니다.'})

    if request.method == 'PUT':
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
    
    elif request.method == 'DELETE':
        comment.delete()
        data = {
            'message': '댓글이 삭제 되었습니다.',
        }
        return Response(data, status.HTTP_204_NO_CONTENT)

def comment_delete(request):
    pass
