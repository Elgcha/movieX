from django.urls import path
from . import views

urlpatterns = [
    # 게시글 전체조회 만들기
    path('', views.community),
    path('create/', views.create),
    path('<int:article_pk>/', views.detail), #게시글 삭제, 수정 통합했음
    # path('<int:article_pk>/update/', views.update),
    # path('<int:article_pk>/delete/', views.delete),
    path('<int:article_pk>/comment/create/', views.comment_create),
    # path('<int:article_pk>/comment/<int:comment_pk>/', views.comment_detail),
    path('<int:article_pk>/comment/<int:comment_pk>/update/', views.comment_update),
    # path('<int:article_pk>/comment/<int:comment_pk>/delete/', views.comment_delete),
]   
