from django.urls import path
from . import views
from django.utils.encoding import uri_to_iri

urlpatterns = [
    ### movie
    path('', views.index),
    path('<int:movie_pk>/', views.movie_detail), #조회,수정, 삭제
    path('create/<int:tmdb_id>/', views.movie_create),
    path('get/date/', views.movie_date), #최신 영화 보여주기
    path('get/random/', views.random_movie),
    path('<int:movie_pk>/same/', views.movie_same), # 비슷한 영화 보여주기 ###추가###

    ### people
    path('people/', views.index_people),
    path('people/create/', views.people_create), #개별적으로 인물을 추가 하고 싶으면
    path('people/<int:people_pk>/', views.people_detail), #조회,수정,삭제
    path('people/<int:people_pk>/movielist/', views.people_movie_list),

   ### 찜 기능
   path('<int:movie_pk>/want/', views.want_movie), #이 영화를 좋아하는 사람들을 출력?
   path('<int:movie_pk>/want/check/', views.want_check),

   ### comment 영화평가 관련
   path('<int:movie_pk>/comment/', views.comment_create),
   path('<int:movie_pk>/<username>/', views.comment_update),
   path('<int:movie_pk>/comment/list/', views.comment_list), #comment에 평점도 보인다
   path('<int:movie_pk>/rate/', views.rate_movie), #DB자체 영화지수 보여주기

   # 장르별 영화리스트 보여주기
   path('<moviename>/', views.list_movie),

   ### API관련
   #영화정보 업데이트 
#path('search/<str:keyword>/', views.search), #검색결과 보여줍니다 #영화리스트를 보여준다 #인물리스트를 보여준다
   path('create/', views.movie_create), #영화 생성 인물이있으면 연결도하자
    #인물과 영화 연결시키는 함수
   path('connect/mtop/', views.people_to_movie), #DB안에 인물과 영화를 연결시킨다
 
   #test
    path('search/<str:keyword>/', views.test), #검색결과 보여줍니다 #영화리스트를 보여준다 #인물리스트를 보여준다

 #영화 추천 알고리즘
    path('<int:user_pk>/test/', views.recommend_for),
    path('<username>/test/recommend/', views.recommend_for),

# ### search
# path(<'search/<str:keyword>/', views.search),

]

