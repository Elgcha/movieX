
# # import requests
# import json
# # from pprint import pprint

# # api_key = '953a5848d0ceb3adab0a2109622b61b6'

# # def get_request_url(method='/movie/popular', **kwargs):
# #     """API 요청에 필요한 주소를 구성합니다.
    
# #     Args:
# #         method: API 서비스에서 제공하는 메서드로써 기본 경로 뒤에 추가됩니다.
# #         **kwargs: 쿼리 스트링 형태로 기본 요청 주소 뒤에 추가됩니다.

# #     Returns:
# #         base_url, 메서드, 쿼리 스트링으로 구성된 요청 주소를 반환합니다.
# #     """
# #     base_url = 'https://api.themoviedb.org/3'
# #     request_url = base_url + method
# #     request_url += f'?api_key={api_key}'

# #     for k, v in kwargs.items():
# #         request_url += f'&{k}={v}'

# #     return request_url


# #     ##################
# # #인기영화 목록 출력
# # my_api = get_request_url(region='KR', language='ko')
# # movie_list = requests.get(my_api).json()

# # movie_database = []
# # for i in range(len(movie_list.get('results'))):
# #     movies = movie_list.get('results')[i]
# #     movie_contents = {
# #         'model': 'movies.Movie',
# #         'pk': i+1,
# #         'fields': {
# #             'title': movies.get('title'),
# #             'release_date': movies.get('release_date'),
# #             'poster_path': movies.get('poster_path'),
# #             'vote_count': movies.get('vote_count'),
# #             'vote_average': movies.get('vote_average'),
# #             'adult': movies.get('adult'),
# #             'original_title': movies.get('original_title'),
# #             'genres': movies.get('genre_ids'),
# #             'overview': movies.get('overview'),
# #             'tmdb_id': movies.get('id'),
# #             'popularity': movies.get('popularity'),
# #         }
# #     }
# #     movie_database.append(movie_contents)



# # movie_list_id = []
# # for movie_id_num in range(0,20):
# #     movie_list_id.append(movie_list.get('results')[movie_id_num].get('id'))   

# # person_database = []
# # pk = 1
# # check_id = []
# # for i in range(20): #샘플로 20개 까지만 range(len(movie_list_id)):
# #     credits_url = get_request_url(method=f'/movie/{movie_list_id[i]}/credits', region='KR', language='ko')
# #     #print(credits_url)
# #     credits_list = requests.get(credits_url).json() 
# #     for j in range(5):
# #         person = credits_list.get('cast')[j]
# #         #print(person)
# #         #order 4까지만 일단 만들어보자
# #         contents = {
# #             'model': 'movies.people',
# #             'pk': pk,
# #             'fields': {
# #                 'name': person.get('name'),
# #                 'popularity': person.get('popularity'),
# #                 'profile_path': person.get('profile_path'),
# #                 'adult': person.get('adult'),
# #                 'gender': person.get('gender'),
# #                 'tmdb_id': person.get('id')
# #             #  'also_known_as': person.get('al')
# #             #  'birthday': get('birthday')
# #             }
# #         }
# #         if person.get('id') in check_id:
# #             continue
# #         check_id.append(person.get('id'))
# #         person_database.append(contents)
# #         pk += 1

# # #print(person_database)
# # person_database_id = []
# # for i in range(len(person_database)):
# #     #print(person_database[i]['fields']['tmdb_id'])
# #     person_database_id.append(person_database[i]['fields']['tmdb_id'])


# # ##########
# # # 인물 상세페이지로 가기 '또다른이름' 추개헛 한글이름도 추가해준거임
# # profile_count = 0
# # for i in person_database_id:
# #     person_api = get_request_url(method=f"/person/{i}") #바이오그라피가 한글로 나올라면 한글설정추가
    
# #     person_profile_database = requests.get(person_api).json() 
# #     #print(person_profile_database)
# #     #person_profile_database['also_known_as']
# #     # print(len(person_database_id))
# #     #pprint(person_database)
# #     person_database[profile_count]['fields']['also_known_as'] = person_profile_database['also_known_as']
# #     profile_count += 1
   
# # # 인물 목록 출력하기
# # with open('people2.json', 'w', encoding='UTF-8') as file:
# #     json.dump(person_database, file, ensure_ascii=False)



# from konlpy.tag import Okt

# with open('movie.json', encoding='UTF-8') as json_file:
#     json_data = json.load(json_file)

# print(json_data[1])

# okt =Okt()
# contents = list(map(lambda x: x['content', json_data]))
# vocab = []
# for content in contents:
#     vocab += okt.nouns(content)
import requests
import json

api_key = '953a5848d0ceb3adab0a2109622b61b6'
def get_request_url(method='movie/popular', **kwargs):
    base_url = 'https://api.themoviedb.org/3/'
    request_url = base_url + method
    request_url += f'?api_key={api_key}'
    for k, v in kwargs.items():
        request_url += f'&{k}={v}'
    return request_url

url = get_request_url(method='person/525626')
data = requests.get(url).json()
data_len = data.get('cast')
dataset = []
update_set =[]
print(url)