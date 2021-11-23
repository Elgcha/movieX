from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('profile/<username>/', views.profile),
    path('profile/<username>/', views.other_profile),
    path('profile/<username>/commentlist/', views.user_comment_set), #한 사람이 영화를 평가한 모든 한줄평
    path('api-token-auth/', obtain_jwt_token),
    path('<username>/follow/', views.follow),
    path('profile/<username>/count', views.user_count), #팔로우,팔로잉, 평가한영화,찜한영화 총횟수
    path('profile/<username>/followlist/', views.follow_list), 

    path('profile/<username>/recommend/', views.user_recommend),

    # temp
    path('profiles/<int:user_pk>/', views.temp),
    path('image/<int:profile_pk>/', views.temp2),


    

    # 로그인이나 업데이트는 vue에서 처리해서 필요 없을듯?
    # path('login/', views.login),
    # path('update/', views.update),
    # path('delete/', views.delete),
    # path('password/', views.password_change),
]
