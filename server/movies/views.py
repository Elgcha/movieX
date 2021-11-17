from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Movie, People, Genre
from .serializers import MovieSerializer, PeopleSerializer


# Create your views here.
@api_view(['GET'])
def index(request): #전체 영화 목록 조회
    if request.method =='GET': #api view로 get을 받는데 if를 안해도 됌? 해야 함?
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def index_people(request): #전체 인물 목록 조회
    if request.method =='GET': 
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data)