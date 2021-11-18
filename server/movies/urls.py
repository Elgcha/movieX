from django.urls import path
from . import views

urlpatterns = [
    ### movie
    path('', views.index),
    path('<int:movie_pk>/', views.movie_detail),
    path('create/', views.movie_create),
   # path('<int:movie_pk>/update/', views.movie_update),

    ### people
    path('people/', views.index_people),
    path('people/create/', views.people_create),
    path('people/<int:people_pk>/', views.people_detail),
   # path('people/<int_peoele_pk/update/', views.people_update),

]
