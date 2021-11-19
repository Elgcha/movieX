from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('profile/<username>/', views.profile),
    path('profile/<username>/', views.other_profile),
    path('api-token-auth/', obtain_jwt_token),
    path('<username>/follow/', views.follow),

    # temp
    path('profiles/<int:user_pk>/', views.temp),
    path('image/<int:profile_pk>/', views.temp2),


    

    # 로그인이나 업데이트는 vue에서 처리해서 필요 없을듯?
    # path('login/', views.login),
    # path('update/', views.update),
    # path('delete/', views.delete),
    # path('password/', views.password_change),
]
