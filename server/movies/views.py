from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils.encoding import uri_to_iri
from django.db.models import Avg
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.serializers import Serializer
from accounts.models import User
from .models import Movie, MovieSite, People, Genre, MovieComment
from .serializers import MovieSerializer, PeopleMovieListSerializer, PeopleSerializer, MovieCommentSerializer, MovieSiteSerializer


import random
import requests
from itertools import chain


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
@permission_classes([AllowAny])
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
@api_view(['GET'])
@permission_classes([AllowAny])
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

def get_search_movie_detail(tmdb_id):#movie_create_api(request, keyword):
    #url을 영화만 보여줄건지 search/multi로 인물도 같이 보여줄건지
    # url = get_request_url(method='search/movie',region='KR', language='ko', query=f'{tmdb_id}')#f'{uri_to_iri(keyword)}' )
    # data = requests.get(url).json()
    # tmdb_id = data['results'][0]["id"]
    # tmdb_id받으면이거만쓰면됌
    url2 = get_request_url(method=f'movie/{tmdb_id}',region='KR', language='ko') #영화라면
    data2= requests.get(url2).json()
    return Response(data2)

def movie_credits(tmdb_id): #인물을 위한 크레딧페이지 불러와서 인물 추출하기
    url = get_request_url(method=f'movie/{tmdb_id}/credits',region='KR', language='ko') 
    data= requests.get(url).json()
    return Response(data)

def people_credits(tmdb_id): #인물 상세정보추가를 위한 인물디테일불러오기
    url = get_request_url(method=f'/person/{tmdb_id}',region='KR', language='ko') 
    data= requests.get(url).json()
    return Response(data)

def people_movie_credits(tmdb_id): #인물 상세정보추가를 위한 인물출연영화목록불러오기
    url = get_request_url(method=f'/person/{tmdb_id}/movie_credits',region='KR', language='ko') 
    data= requests.get(url).json()
    return Response(data)

@api_view(['GET',"POST"]) #불러와서저장하는 함수 #영화를 불러오면 인물도 같이 가져와서저장해주자
def db_update(request, keyword):#movie_save(request,keyword):

    if request.user.is_superuser:      
        if Movie.objects.filter(tmdb_id=keyword):
            data = {
                'message': '이미 저장되어있는 영화입니다.'
            }
            return Response(data, status=status.HTTP_208_ALREADY_REPORTED)
        else:
            data = get_search_movie_detail(keyword) #영화라면
            mpk = Movie.objects.count() +1
            genre = []
            for i in data.data.get('genres'):
                genre.append(i.get('id'))

            created = Movie.objects.create(
                    id = mpk,   
                    adult = data.data.get('adult'),
                    backdrop_path = data.data.get('backdrop_path'),
                    tmdb_id= data.data.get('id'),
                    original_title= data.data.get('original_title'),
                    overview= data.data.get('overview'),
                    popularity = data.data.get('popularity'),
                    poster_path =  data.data.get('poster_path'),
                    release_date = data.data.get('release_date'),
                    runtime = data.data.get('runtime'),
                    title = data.data.get('title'),
                    vote_average = data.data.get('vote_average'),
                    vote_count = data.data.get('vote_count')
                )
            created.genres.set(genre)
            created.save()
    #인물저장하기
            credits = movie_credits(keyword)
            person_id = []
            for i in range(5): #일단은 5명만
                data = credits.data.get('cast')[i]

                if People.objects.filter(tmdb_id=data.get('id')): #에러임 없다는걸알아야됌v필터;;
                    created_people = People.objects.get(tmdb_id=data.get('id'))
                    pk = created_people
                else:
                    pk = People.objects.count()+1
                    created_people = People.objects.create(
                        id = pk,   
                        name = data.get('name'),
                        popularity = data.get('popularity'),
                        tmdb_id= data.get('id'),
                        birthday= data.get('birthday'),
                        profile_path= data.get('profile_path'),
                        adult = data.get('adult'),
                        gender = data.get('gender'),
                        also_known_as = data.get('also_known_as'),
                        known_for_department = data.get('known_for_department')
                        )
                    created_people.save()
                created_one = Movie.objects.get(pk=mpk)
                created_one.people.add(created_people)
                created_one.save()

                person_id.append(data.get('id')) #영화에 추가된 인물

            for j in person_id:
            ## 인물 추가정보 저장
                person = People.objects.get(tmdb_id=j)
                people_add = people_credits(j).data
                person.also_known_as = people_add.get('also_known_as')
                person.birthday = people_add.get('birthday')
                person.save()
        return Response(status=status.HTTP_201_CREATED)     
    else:
        data = {
                'message': '권한이 없습니다.'
            }
        return Response(data)

#슈퍼유저아닐경우 메세지추가
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
    movie_set= set()
    for i in movie.genres.all():
        id = i.id
        movie_list.append(id)
    for j in movie_list:
        movie = Movie.objects.filter(genres=j).exclude(pk=movie_pk)
        movie_set.add(movie)
    result = list(chain.from_iterable(movie_set))
    print(result)
    serializer = MovieSerializer(result, many=True)
    return Response(serializer.data)

### for people

@api_view(['GET'])
@permission_classes([AllowAny])
def index_people(request): #전체 인물 목록 조회
    if request.method =='GET': 
        people = People.objects.all()
        serializer = PeopleSerializer(people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET','PUT','DELETE'])
def people_detail(request, people_pk):
    people = get_object_or_404(People, pk=people_pk)

    if request.method == 'GET':
        serializer = PeopleSerializer(people)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # if request.method == "PUT":
    #     serializer = MovieSerializer(people, data = request.data)
    #     if serializer.is_valid(raise_exception=True):
    #         serializer.save(people=people)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    
    # if request.method == "DELETE":
    #     people.delete()
    #     data = {
    #         'message': '영화가 삭제 되었습니다',
    #     }
    #     return Response(data, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def people_movie_list(request, people_pk):
    people = get_object_or_404(People, pk=people_pk)
    serializer = PeopleMovieListSerializer(people)
    return Response(serializer.data, status=status.HTTP_200_OK)

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

## 내가평가하모든 영화의유사성
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
                    data[f'{rated}']['rate'] + #내가 평가한 영화의 평점
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

@api_view(['GET'])
@permission_classes([AllowAny])
def site_get(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    moviesites = MovieSite.objects.filter(movie=movie)
    serializer = MovieSiteSerializer(moviesites, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def site_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = MovieSiteSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user, movie=movie)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['DELETE'])
def site_delete(request, movie_pk, site_id):
    moviesite = get_object_or_404(MovieSite, pk=site_id)
    moviesite.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

