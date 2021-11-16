from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Movie, People, Genre
from .serializers import MovieSerializer


# Create your views here.
@api_view(['GET'])
def index(request):
    if request.method =='GET': #api view로 get을 받는데 if를 안해도 됌? 해야 함?
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)