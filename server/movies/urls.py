from django.urls import path
from . import views

urlpatterns = [
    ### movie
    path('', views.index),
    path('<int:movie_pk>/', views.movie_detail),
    path('create/', views.movie_create),
    path('get/date/', views.movie_date),
   # path('<int:movie_pk>/update/', views.movie_update),

    ### people
    path('people/', views.index_people),
    path('people/create/', views.people_create),
    path('people/<int:people_pk>/', views.people_detail),
   # path('people/<int_peoele_pk/update/', views.people_update),

   ### comment
   path('<int:movie_pk>/comment/', views.comment_create),
   path('<int:movie_pk>/<int:moviecomment_pk>/', views.comment_update),
   path('<int:movie_pk>/commentlist/', views.comment_list), #comment에 평점도
   #path('<int:movie_pk>/rate/', views.rate_movie),

   ### 찜 기능
   path('<int:movie_pk>/want/', views.want_movie), #이 영화를 좋아하는 사람들을 출력?
   path('<int:movie_pk>/want/check/', views.want_check),

   path('<int:movie_pk>/likes/', views.likes_movie),

#영화코멘트관련
#보고싶은영화


# ### search
# path(<'search/<str:keyword>/', views.search),
]

