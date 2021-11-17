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
            'movie_id': movies.get('id'),
            'title': movies.get('title'),
            'release_date': movies.get('release_date'),
            'poster_path': movies.get('poster_path'),
            'vote_count': movies.get('vote_count'),
            'vote_average': movies.get('vote_average'),
            'adult': movies.get('adult'),
            'original_title': movies.get('original_title'),
            'overview': movies.get('overview'),
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

#print(movie_list_id)