from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from community.serializers import CommentSerializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Movie, People, Genre, MovieComment
from .serializers import MovieSerializer, PeopleSerializer, MovieCommentSerializer
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
        serializer = PeopleSerializer(people)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "PUT":
        serializer = MovieSerializer(people, data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(people=people)
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    if request.method == "DELETE":
        people.delete()
        data = {
            'message': '영화가 삭제 되었습니다',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)

def people_update(request):
    pass

### comment
@api_view(['POST'])
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk= movie_pk)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def comment_list(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comments = movie.moviecomment_set.all()
    serializer = MovieCommentSerializer(comments, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PUT','DELETE'])
def comment_update(request, movie_pk, moviecomment_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = movie.moviecomment_set.get(pk= moviecomment_pk)

    if request.method == 'GET':  # 조회
        serializer = MovieCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == 'PUT': # 수정
        serializer= MovieCommentSerializer(comment, data=request.data) 
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    if request.method == 'DELETE': # 삭제
        comment.delete()
        data = {
            'message': '평가가 삭제 되었습니다.',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)
   
### want
@api_view(['POST'])
def want_movie(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.want.filter(pk=request.user.pk).exists():
        movie.want.remove(request.user)
        wanted = False
    else:
        movie.want.add(request.user)
        wanted = True
    data = {
        'wanted' : wanted,
        'count' : movie.want.count(), #영화 찜한 사람수
    }
    return Response(data)

@api_view(['GET']) #비슷한 영화 찾기
def likes_movie(request, movie_pk):
    '''
    영화 
    '''
    movies = Movie.objects.all() #
    serializer = MovieSerializer(movies, many=True)
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_code = movie.tmdb_id
    #임시
    url =f'https://api.themoviedb.org/3/movie/{movie_code}/similar?api_key=953a5848d0ceb3adab0a2109622b61b6&region=KR&language=ko'
    data = requests.get(url).json()
    movies.filter(tmdb_id='movie')
    for choice in data.get('results'):
        choice.get('id') in movies.

    return Response(data)



# #### search
# def search(request, keyword):
#     movie = Movie.objects.all()
#     people = People.objects.all()
#     genre = Genre.objects.all()
#     if keyword in  movie:
#         k = movie.find('keyword')
#     request_url = get_request_url('/search/movie', query=title, region='KR', language='ko')
#     data = requests.get(request_url).json()
#     results = data.get('results')
#     if results:
#         movie = results[0]
#         movie_id = movie['id']
#         return movie_id
#     else:
#         return None