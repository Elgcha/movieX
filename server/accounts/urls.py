from django.urls import path
from . import views
from rest_framework_jwt.views import obtain_jwt_token

urlpatterns = [
    path('signup/', views.signup),
    path('profile/', views.profile),
    path('api-token-auth/', obtain_jwt_token),
    path('<username>/follow', views.follow),

    

    # 로그인이나 업데이트는 vue에서 처리해서 필요 없을듯?
    # path('login/', views.login),
    # path('update/', views.update),
    # path('delete/', views.delete),
    # path('password/', views.password_change),
]
