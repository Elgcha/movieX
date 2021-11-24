from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import uri_to_iri
from django.db.models import Avg
from django.contrib.auth import get_user_model
from requests import api
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from accounts.models import User
from .models import Movie, People, Genre, MovieComment
from .serializers import MovieSerializer, PeopleMovieListSerializer, PeopleSerializer, MovieCommentSerializer, Movie2Serializer

import random
import requests

from movies import serializers


# Create your views here.
## api 관련
api_key = '953a5848d0ceb3adab0a2109622b61b6'
def get_request_url(method='movie/popular', **kwargs):
    base_url = 'https://api.themoviedb.org/3/'
    request_url = base_url + method
    request_url += f'?api_key={api_key}'
    for k, v in kwargs.items():
        request_url += f'&{k}={v}'
    return request_url
### 이 두 함수는 데이터베이스의 값을 갱신하는 함수이다
## movie connect people
# 빈리스트 가져와서 비교하는 방식으로바꿔보자 #
## 가져온 영화값에 인물이 연결되어있지 않다.
## 인물 크레딧에 영화정보가 있고 그걸 연결한다
@api_view(['GET'])
def people_to_movie(request): 
    movies = Movie.objects.all()
    people = People.objects.all()
    movieset = []
    for movie_code in movies:
        movieset.append(movie_code.tmdb_id)
    # 사람의 id값을 조회해서 영화목록을 가져오자
    for person_code in people:
        person = People.objects.get(tmdb_id=person_code.tmdb_id)
        url = get_request_url(method=f'person/{person_code.tmdb_id}/movie_credits')
        data = requests.get(url).json()
        dataset = []
        update_set =[]
      # 출연한영화 목록을 리스트로 만들어준다.  
        for i in range(len(data.get('cast'))):
            dataset.append(data.get('cast')[i].get('id'))
        for j in movieset:
            if j in dataset:
                update_set.append(j)
        for k in update_set:
            movie = Movie.objects.get(tmdb_id=k)
            movie.people.add(person)
    return Response(status=status.HTTP_200_OK)

#전체영화의 변동정보 업데이트
def movie_update(request):
    movies = Movie.objects.all()
    for i in movies:
        url = get_request_url(f'movie/{i.tmdb_id}')
        data = requests.get(url).json()
        movie = Movie.objects.get(tmdb_id=i.tmdb_id)
        movie.popularity = data.get('popularity')
        movie.vote_average = data.get('vote_average')
        movie.vote_count = data.get('vote_count')
        movie.runtime = data.get('runtime')
        movie.save()
    return Response(status=status.HTTP_200_OK)
###

# 영화검색 시리얼라이저로 보여줌
# @api_view(['GET'])
# def test(request, keyword):#movie_create_api(request, keyword):
#     #url을 영화만 보여줄건지 search/multi로 인물도 같이 보여줄건지
#     url = get_request_url(method='search/movie',region='KR', language='ko', query=f'{uri_to_iri(keyword)}' )
#     data = requests.get(url).json()
#     tmdb_id = data['results'][0]["id"]
#     print(tmdb_id)
#     return tmdb_id

def tests(keyword):#movie_create_api(request, keyword):
    #url을 영화만 보여줄건지 search/multi로 인물도 같이 보여줄건지
    url = get_request_url(method='search/movie',region='KR', language='ko', query=f'{keyword}')#f'{uri_to_iri(keyword)}' )
    data = requests.get(url).json()
    tmdb_id = data['results'][0]["id"]
    url2 = get_request_url(method=f'movie/{tmdb_id}')
    data2= requests.get(url2).json()
    return Response(data2)

@api_view(['GET'])
def test(request, keyword):#movie_save(request,keyword):
    data = tests(f'{uri_to_iri(keyword)}')
    serializer = Movie2Serializer(data.data)
    return Response(serializer.data)

## 검색해서 영화json 까지는 가져옴, 이 json을 어떻게 저장시킬꺼냐가 필요하다

## 영화검색한거 받아서 저장하기
@api_view(['POST'])
def test2(request):
    serialzer = MovieSerializer(data = request.data)


##

##
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
def movie_create(request, tmdb_id):
    serializer = MovieSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def movie_date(request):
    movies = Movie.objects.order_by('-release_date')[:20]
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

### 비슷한 영화 보여주기
# 장르로 필터
@api_view(['GET'])
@permission_classes([AllowAny])
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
    if movie.moviecomment_set.filter(user=request.user):
        return Response(status=status.HTTP_200_OK)
    serializer = MovieCommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(movie=movie, user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

#영화별 자체 알고리즘을 통한 영화지수 보여주기
@api_view(['GET'])
@permission_classes([AllowAny])
def rate_movie(request, movie_pk):
    
    movie = get_object_or_404(Movie, pk=movie_pk)
    if movie.moviecomment_set.count():
        rate_ratio = movie.moviecomment_set.aggregate(Avg('rate')).get('rate__avg') * 0.8
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
def comment_update(request, movie_pk, username):
    User = get_user_model()
    person = get_object_or_404(User, username=username)
    if person != request.user:
        return Response(status.HTTP_401_UNAUTHORIZED)
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment = movie.moviecomment_set.get(user=person)

    # if request.method == 'GET':  # 조회
    #     serializer = MovieCommentSerializer(comment)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

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





                  
@api_view(['GET'])
@permission_classes([AllowAny])
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
from django.db.models import Q
@api_view(['GET'])
@permission_classes([AllowAny])
def random_movie(request):
    movies = Movie.objects.all()
    moviecomments = MovieComment.objects.filter(user=request.user)
    # for movie in movies:
    for moviecomment in moviecomments:
        movies = movies.filter(~Q(pk=moviecomment.movie_id))
    if not movies:
        return Http404
    movie = random.choice(movies)
    serializer = MovieSerializer(movie)
    return Response(serializer.data)




# 장르의 유사도를 구해서
# 인기도와 유저 평점에 결과값을 곱하자
import operator
def jaccrdsimilarity(A, B):
    a = A.genres.all()
    b = B.genres.all()
    mom = a.union(b).count()
    son = a.intersection(b).count()
    return round(son/mom,2)

def extract_sim(user_pk): #한 영화의 모든영화의 유사도
    movie_on = Movie.objects.get(pk=user_pk)
    A = movie_on
    movies = Movie.objects.count()
    sim = {
        'movie':A.title,
            'id':A.pk
        }
    for m in range(1, movies+1):
        if m == user_pk:
            continue
        movie = Movie.objects.get(pk=m)
        B = movie
        sim[f'{movie.pk}'] = {
            'id': movie.id,
            'title': movie.title,
            'poster_path': movie.poster_path,
            'similarity': jaccrdsimilarity(A,B),
            }
    return sim
### 영화의 유사성으로 추천페이지 구성하기
##############################
#내가 평가한 모든 영화의 유사성을 구한다
def extract(username):
    user = get_object_or_404(get_user_model(),username=username)
    all_rate = user.moviecomment_set.all()
    all_sims = [] #평가한 영화를 기준으로 모드영화의 유사성을 나타낸 것
    #평가한 모든영화의 유사성을 담는다
    for i in all_rate:
        all_sims.append(extract_sim(i.movie.pk)) 
    return all_sims
#####
## 내가평가하모든 영화의유사성
###
def extract_recommend(username):
    user = get_object_or_404(get_user_model(),username=username)
    all_rate = user.moviecomment_set.all()
    all_sims = extract(username)
    data =  {} #내가 평가한 영화
    for value in all_rate:
        data[f'{value.movie.id}'] = {
            'id': value.movie.id,
            'title': value.movie.title,
            'rate': value.rate,
            }
##모든 영화의 유사성에서 추천값 구하기
    #모든영화의 유사성 값에 내가 평가한 영화의 평점이랑 인기도, 평점을 곱해서 나타낸다.
    for j in all_sims:
         for rated in range(1, Movie.objects.all().count()+1): #모든 영화 아이디
             if f'{rated}' in data and f'{rated}' not in j: #sim에 영화아이디가 없다면 추천받을 영화임
                for result in j:
                    if result == 'movie' or result =='id':
                        continue
                    j[result]['recommend'] = round((  
                    j[result]['similarity'] *    #내가 평가한 영화와의 유사도
                    data[f'{rated}']['rate'] * #내가 평가한 영화의 평점
                    Movie.objects.get(pk= f'{result}').vote_average # 이 영화의 db 평점
                    # Movie.objects.get(pk= f'{rated}').popularity #내가 평가한영화의 인기도
                ),3)
    return(all_sims) # 모든영화의 유사도를 구하고
###################################


    ##### 높은 순으로 필터 하기
    ##리커멘드로 정렬
def recommend_sort(username):
    all_sims = extract_recommend(username)
    # print(all_sims)
    temp_sort = []
    for k in all_sims:
        for result in k:
            if result == 'movie' or result =='id':
                continue
            temp_sort.append(k[result])
    result_sort = sorted(temp_sort, key =operator.itemgetter('recommend'),reverse=True)

    recommendation =[]
    title_temp =[]
    for p in result_sort[:20]:
        if p['title'] not in title_temp:
            recommendation.append(p)
            title_temp.append(p['title'])
    return recommendation

# 추천api보낼 함수:
@api_view(['GET'])
@permission_classes([AllowAny])
def recommend_for(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    data = recommend_sort(username)
    if not data:
        movie = Movie.objects.order_by('-pk')[:10]
        serializer = MovieSerializer(movie, many=True)
        return Response(serializer.data)
        
    return Response(data)
# #무비아이디/ 포스터패스
