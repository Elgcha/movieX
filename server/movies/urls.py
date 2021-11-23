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
    path('<int:movie_pk>/update/', views.movie_update),
    path('<int:movie_pk>/same/', views.movie_same), # 비슷한 영화 보여주기 ###추가###


    ### people
    path('people/', views.index_people),
    path('people/create/', views.people_create),
    path('people/<int:people_pk>/', views.people_detail), #조회,수정,삭제
    path('people/<int:people_pk>/movielist/', views.people_movie_list),
   # path('people/<int_peoele_pk/update/', views.people_update),

   ### 찜 기능
   path('<int:movie_pk>/want/', views.want_movie), #이 영화를 좋아하는 사람들을 출력?
   path('<int:movie_pk>/want/check/', views.want_check),
   ### comment
   path('<int:movie_pk>/comment/', views.comment_create),
   path('<int:movie_pk>/<username>/', views.comment_update),
   path('<int:movie_pk>/comment/list/', views.comment_list), #comment에 평점도
   path('<int:movie_pk>/rate/', views.rate_movie),



   # 장르별 영화리스트 보여주기
   path('<moviename>/', views.list_movie),



    #인물과 영화 연결시키는 함수

   path('connect/mtop/', views.people_to_movie),

#    path('<int:movie_pk>/likes/', views.likes_movie),

#영화코멘트관련
#보고싶은영화

    path('<username>/test/recommend/', views.recommend_for),
    # path('test/test/', views.extract_all),
# ### search
# path(<'search/<str:keyword>/', views.search),
]

