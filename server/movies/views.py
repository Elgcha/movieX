from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Movie, People, Genre
from .serializers import MovieSerializer, PeopleSerializer
from rest_framework.permissions import AllowAny


# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request): #전체 영화 목록 조회
    if request.method =='GET': #api view로 get을 받는데 if를 안해도 됌? 해야 함?
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if request.method == 'GET':
        serialzer = MovieSerializer(movie)
        return Response(serialzer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        serialzer = MovieSerializer(movie, data = request.data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save(movie=movie)
            return Response(serialzer.data,  status=status.status.HTTP_200_OK)
    
    if request.method == "DELETE":
        movie.delete()
        data = {
            'message': '영화가 삭제 되었습니다',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
@api_view(['POST'])
def movie_create(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

def movie_update(request, movie_pk):
    pass

### for people

@api_view(['GET'])
@permission_classes([AllowAny])
def index_people(request): #전체 인물 목록 조회
    if request.method =='GET': 
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
def people_create(request):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
@api_view(['GET','PUT','DELETE'])
def people_detail(request, people_pk):
    people = get_object_or_404(People, pk=people_pk)

    if request.method == 'GET':
        serialzer = PeopleSerializer(people)
        return Response(serialzer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        serialzer = MovieSerializer(people, data = request.data)
        if serialzer.is_valid(raise_exception=True):
            serialzer.save(people=people)
            return Response(serialzer.data, status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        people.delete()
        data = {
            'message': '영화가 삭제 되었습니다',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

def people_update(request):
    pass