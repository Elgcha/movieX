from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('<username>/follow/', views.follow), #팔로우 하기
    path('profile/get/self/', views.profile_self), #프로필 조회
    path('profile/<username>/', views.profile), #프로필 조회
    path('profile/<username>/commentlist/', views.user_comment_set), #한 사람이 영화를 평가한 모든 한줄평
    path('profile/<username>/recommend/', views.user_recommend), #한 사람이 평가한 모든영화
    path('profile/<username>/count/', views.user_count), #팔로우,팔로잉, 평가한영화,찜한영화 총횟수 조회
    path('profile/<username>/follow/list/', views.follow_list),
    path('api-token-auth/', obtain_jwt_token),
    path('profiles/<username>/', views.image),
    path('<username>/update/', views.email_change),
    path('check/', views.admin_check),
]
