from django.http import response
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
import requests
from community.serializers import CommentSerializer
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from accounts.serializers import RecommendSerializer
from .models import Movie, People, Genre, MovieComment
from .serializers import MovieSerializer, PeopleMovieListSerializer, PeopleSerializer, MovieCommentSerializer
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from django.utils.encoding import uri_to_iri
from django.db.models import Avg

# Create your views here.
@api_view(['GET'])
@permission_classes([AllowAny])
def index(request): #전체 영화 목록 조회
    if request.method =='GET': 
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

@api_view(['GET','PUT','DELETE'])
@permission_classes([AllowAny])
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

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_date(request):
    movies = Movie.objects.order_by('-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

### 비슷한 영화 보여주기
# 장르로 필터
@api_view(['GET'])
def movie_same(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    movie_list = []
    movie_set=[]
    for i in movie.genres.all():
        id = i.id
        movie_list.append(id)
    for j in movie_list:
        movie = Movie.objects.filter(genres=j).exclude(pk=movie_pk)
        movie_set.append(movie)
    serializer = MovieSerializer(movie, many=True)
    return Response(serializer.data)


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

@api_view(['GET'])
def people_movie_list(request, people_pk):
    people = get_object_or_404(People, pk=people_pk)
    serializer = PeopleMovieListSerializer(people)
    return Response(serializer.data, status=status.HTTP_200_OK)
       
def people_update(request):
    pass

### comment
@api_view(['POST'])
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk= movie_pk)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#영화별 자체 알고리즘을 통한 영화지수 보여주기
@api_view(['GET'])
def rate_movie(request, movie_pk):
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.moviecomment_set.count():
        rate_ratio = movie.moviecomment_set.aggregate(Avg('rate')).get('rate__avg') * 0.6
    else:
        rate_ratio = 3

    vote_ratio = movie.vote_average * 0.4 
    pop_ratio = movie.popularity * 0.1 / movie.vote_count
    score = round(rate_ratio + vote_ratio+ pop_ratio,1)
    data = {
        "score": score, #영화지수
        'rate':rate_ratio, #평점가중치
        'vote':vote_ratio, #api평점 가중치
        'pop':pop_ratio, #api 인기도 가중치
    }
    # api업데이트기능을 추가해서 실시간 업데이트 가능
    return Response(data)



@api_view(['GET'])
@permission_classes([AllowAny])
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

@api_view(['POST'])
def want_check(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.want.filter(pk=request.user.pk).exists():
        wanted = True
    else:
        movie.want.add(request.user)
        wanted = False
    data = {
        'wanted' : wanted,
        'count' : movie.want.count(), #영화 찜한 사람수
    }
    return Response(data)


## movie connect people
# 빈리스트 가져와서 비교하는 방식으로바꿔보자 #
## 가져온 영화값에 인물이 연결되어있지 않다.
## 인물 크레딧에 영화정보가 있고 그걸 연결한다
def people_to_movie(request): #get_objects_404로바꿀수잇으면 바꾸자
    movies = Movie.objects.all()
    people = People.objects.all()
    # 사람의 id값을 조회해서 영화목록을 가져오자
    for person_code in people:
        url =f'https://api.themoviedb.org/3/person/{person_code.tmdb_id}/movie_credits?api_key=953a5848d0ceb3adab0a2109622b61b6&region=KR&language=ko'
        data = requests.get(url).json()
        dataset = data.get('cast')

        person = People.objects.get(tmdb_id=person_code.tmdb_id)
        movieset = []
      # 출연한영화 목록을 리스트로 만들어준다.  
        for i in range(len(dataset)):
            movieset.append(data.get('cast')[i].get('id'))
        #만들어진 리스트에서 db에 맞는 영화가 있는지 찾는다.
            for j in movieset:
                if movies.filter(tmdb_id=j):
                    movie = Movie.objects.get(tmdb_id=j)
                    movie.people.add(person)
                    # print(movies)
    #                 # update = movies.objects.get(tmdb_id=j)
    #                 # update.people += person_code
    #                 # update.save()
    return Response(status=status.HTTP_200_OK)
                  
@api_view(['GET'])
def list_movie(request, moviename):
    if uri_to_iri(moviename) == '대문':
        movies = Movie.objects.order_by('-popularity', '-vote_average')[:5]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    if uri_to_iri(moviename) == '평점순':
        movies = Movie.objects.order_by('-vote_average')[:20]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    if uri_to_iri(moviename) == '인기':
        movies = Movie.objects.order_by('-popularity')[:20]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)

    else: #장르 검색 결과
        genre = Genre.objects.get(name=uri_to_iri(moviename))
        movies = Movie.objects.filter(genres=genre).order_by('-popularity')[:20]
        serializer = MovieSerializer(movies, many=True)

        return Response(serializer.data)


# ###
# import pandas as pd
# import math
# import numpy as np
# import operator

# def create_table(db):
# #모든 영화 리스트와
# #사람의 평가 항목을 합쳐
#     data = {}
#     for i in db:
#         if i.user.pk not in data.keys():
#             data[i.user.pk]={}

# import numpy as np
# import math
# from numpy import dot
# from numpy.linalg import norm
# import operator

# def cos_sim(A, B):
#   return dot(A, B)/(norm(A)*norm(B))

# def cosine_similarity(A,B):
#     A_norms = B_norms = 0
#     dot_p = np.dot(A,B)
#     A_norms = math.sqrt(sum([i**2 for i in A]))
#     B_norms = math.sqrt(sum([i**2 for i in B]))
#     AB_norms = A_norms * B_norms
#     return dot_p / AB_norms # 1에 가까울수록 유사함.

# @api_view(['GET','POST'])
# def extract(request, user_pk):
#     movies = MovieComment.objects.filter(user=user_pk)
#     movie_data = {}
#     for i in movies:
#         if i.user.pk not in movie_data.keys():
#             movie_data[i.user.pk] = {i.movie.pk:float(i.rate)}
#         else:
#             movie_data[i.user.pk].setdefault(i.movie.pk, float(i.rate))


#     return Response(movie_data, status=status.HTTP_200_OK)


#   # 한영화의 데이터를 기준으로 내가평가한 모든영화의 유사도를 구합니다
# @api_view(['GET','POST'])
# def extract_all(request):
#     movies = MovieComment.objects.all()
#     movie_data = {}
#     for i in movies:
#         if i.user.pk not in movie_data.keys():
#             movie_data[i.user.pk] = {i.movie.pk:float(i.rate)}
#         else:
#             movie_data[i.user.pk].setdefault(i.movie.pk, float(i.rate)) 
#     my_rating = set(movie_data[1].keys())
#     similar_score={} # 사용자간 유사도 결과.
#     for you in movie_data.keys():
#         if you != 1:
#             you_rating = set(movie_data[you].keys())
#             # (2) 나와 상대방의 교집합(intersection)를 찾는다.
#             intersect = my_rating.intersection(you_rating)
#             # (3) 겹치는게 최소 갯수 이상인 경우에만 유사도 측정 시작 
#             #if len(intersect) >= 3:  
#             # (4) 상대방과 나의 겹치는 영화의 평점을 추출해낸다
#             my_rating_score = [movie_data[1][i] for i in intersect]
#             you_rating_score = [movie_data[you][i] for i in intersect]
#             # 2개의 데이터를 통해 유사도를 측정
#             score = cosine_similarity(my_rating_score, you_rating_score)

#             similar_score[you]=score

#     # return Response(movie_data, status=status.HTTP_200_OK)
#     return Response(similar_score, status=status.HTTP_200_OK)



    
