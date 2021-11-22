import requests
import json
from pprint import pprint

api_key = '953a5848d0ceb3adab0a2109622b61b6'

def get_request_url(method='/movie/popular', **kwargs):
    """API 요청에 필요한 주소를 구성합니다.
    
    Args:
        method: API 서비스에서 제공하는 메서드로써 기본 경로 뒤에 추가됩니다.
        **kwargs: 쿼리 스트링 형태로 기본 요청 주소 뒤에 추가됩니다.

    Returns:
        base_url, 메서드, 쿼리 스트링으로 구성된 요청 주소를 반환합니다.
    """
    base_url = 'https://api.themoviedb.org/3'
    request_url = base_url + method
    request_url += f'?api_key={api_key}'

    for k, v in kwargs.items():
        request_url += f'&{k}={v}'

    return request_url


def get_movie_id(title):
    """영화 제목을 이용하여 아이디를 추출합니다.

    영화 제목을 이용하여 TMDB API 서버에 요청을 보내고 
    응답 결과에서 해당 영화의 id 값을 반환합니다.

    Args:
        title: 영화 제목.
    
    Returns:
        영화 아이디(id)를 반환합니다.
        단, 응답 결과가 없을 경우 None을 반환합니다.
    """
    request_url = get_request_url('/search/movie', query=title, region='KR', language='ko')
    data = requests.get(request_url).json()
    results = data.get('results')
    if results:
        movie = results[0]
        movie_id = movie['id']
        return movie_id
    else:
        return None
'''
k = get_request_url('/movie/634649', region='KR', language='ko')
print(k)
print(requests.get(k).json())
'''

##################
#인기영화 목록 출력
my_api = get_request_url(region='KR', language='ko')
movie_list = requests.get(my_api).json()

movie_database = []
for i in range(len(movie_list.get('results'))):
    movies = movie_list.get('results')[i]
    movie_contents = {
        'model': 'movies.Movie',
        'pk': i+1,
        'fields': {
            'title': movies.get('title'),
            'release_date': movies.get('release_date'),
            'poster_path': movies.get('poster_path'),
            'vote_count': movies.get('vote_count'),
            'vote_average': movies.get('vote_average'),
            'adult': movies.get('adult'),
            'original_title': movies.get('original_title'),
            'genres': movies.get('genre_ids'),
            'overview': movies.get('overview'),
            'tmdb_id': movies.get('id'),
            'popularity': movies.get('popularity'),
        }
    }
    movie_database.append(movie_contents)

#pprint(movie_database)

with open('movies.json', 'w', encoding='UTF-8') as file:
    json.dump(movie_database, file, ensure_ascii=False)

###########################

# 인기영화 아이디 값만 추출 하기
movie_list_id = []
for movie_id_num in range(0,20):
    movie_list_id.append(movie_list.get('results')[movie_id_num].get('id'))
    #pprint(movie_list_id)


######## 장르 추출하기

genre_url = get_request_url(method='/genre/movie/list', region='KR', language='ko')
genre_list = requests.get(genre_url).json()
genre_database = []
for i in range(len(requests.get(genre_url).json().get('genres'))):
    genre = genre_list.get('genres')[i]
    contents = {
        'model': 'movies.genre',
        'pk': genre.get('id'),
        'fields': {
            'name': genre.get('name'),
        }
    }
    genre_database.append(contents)

#print(genre_url) 장르목록 출력하기
with open('genre.json', 'w', encoding='UTF-8') as file:
    json.dump(genre_database, file, ensure_ascii=False)


#######
# 인물 db를 가져오고, 인물db와 영화 db를 이어줘야한다.
# 영화db에서 영화id를 가져오고 그영화를 조회해서 인물 목록 추출하고, 
# 그 인물 목록의 db를 저장하자
####### 인물 db저장
person_database = []
pk = 1
check_id = []
for i in range(20): #샘플로 20개 까지만 range(len(movie_list_id)):
    credits_url = get_request_url(method=f'/movie/{movie_list_id[i]}/credits', region='KR', language='ko')
    #print(credits_url)
    credits_list = requests.get(credits_url).json() 
    for j in range(5):
        person = credits_list.get('cast')[j]
        #print(person)
        #order 4까지만 일단 만들어보자
        contents = {
            'model': 'movies.people',
            'pk': pk,
            'fields': {
                'name': person.get('name'),
                'popularity': person.get('popularity'),
                'profile_path': person.get('profile_path'),
                'adult': person.get('adult'),
                'gender': person.get('gender'),
                'tmdb_id': person.get('id')
            #  'also_known_as': person.get('al')
            #  'birthday': get('birthday')
            }
        }
        if person.get('id') in check_id:
            continue
        check_id.append(person.get('id'))
        person_database.append(contents)
        pk += 1

#print(person_database)
person_database_id = []
for i in range(len(person_database)):
    #print(person_database[i]['fields']['tmdb_id'])
    person_database_id.append(person_database[i]['fields']['tmdb_id'])


##########
# 인물 상세페이지로 가기 '또다른이름' 추개헛 한글이름도 추가해준거임
profile_count = 0
for i in person_database_id:
    person_api = get_request_url(method=f"/person/{i}") #바이오그라피가 한글로 나올라면 한글설정추가
    
    person_profile_database = requests.get(person_api).json() 
    #print(person_profile_database)
    #person_profile_database['also_known_as']
    # print(len(person_database_id))
    #pprint(person_database)
    person_database[profile_count]['fields']['also_known_as'] = person_profile_database['also_known_as']
    profile_count += 1
   
# 인물 목록 출력하기
with open('people.json', 'w', encoding='UTF-8') as file:
    json.dump(person_database, file, ensure_ascii=False)

