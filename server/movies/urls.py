from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('people/', views.index_people),
]
