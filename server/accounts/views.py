from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from movies.models import MovieComment
from movies.serializers import MovieCommentSerializer

from .models import User
from .serializers import MovieCommentListSerializer, RecommendSerializer, UserSerializer
from django.contrib.auth import get_user, get_user_model
from rest_framework.permissions import AllowAny
# Create your views here.

#### user #####################################
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # Client에서 데이터 받아오기
    password = request.data.get('password')
    passwordConfirmation = request.data.get('passwordConfirmation')

    # 일치여부 확인
    if password != passwordConfirmation:
        return Response({ ' error': '비밀번호가 일치하지 않습니다.'})

	#UserSerializer를 통해 데이터 직렬화

    serializer = UserSerializer(data=request.data)
    
        #validation 작업 진행 -> password도 같이 직렬화 진행
    if serializer.is_valid(raise_exception=True):
        user = serializer.save()
        #비밀번호 해싱 후 
        user.set_password(request.data.get('password'))
        user.save()
        # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
        return Response(serializer.data, status=status.HTTP_201_CREATED)


#####################프로필 페이지 구성할거 가져오기 
########마이 프로필이랑 다른사람의 프로필하려고 구별했는데 합쳐도 될듯
@api_view(['GET'])
@permission_classes([AllowAny])
def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)
#############################################

@api_view(['POST'])
def follow(request, username):
    #팔로우할 대상
    # person = get_object_or_404(get_user_model(), pk= user_pk)
    person = get_object_or_404(get_user_model(), username=username)
     
    #나
    user = request.user
    if person != user:
        if user.followers.filter(pk=person.pk).exists():
            person.followers.remove(user)
            isFollowed = False
        else:
            person.followers.add(user)
            isFollowed = True
        data = {
            'isFollowed': isFollowed,
            'followers_count': person.followers.count(),
            'followings_count': person.followings.count(),
        }
        return Response(data)
    else:
        data = {
            'message': '자기 자신을 팔로우 할 수 없습니다.',
        }
        return Response(data)#, status=status.)

#유저의 영화평가 리스트 
# 영화이름, 평점, 코멘트 출력함
@api_view(['GET'])
def user_comment_set(request, username):
    comments = get_object_or_404(get_user_model(), username=username)
    serialzer = MovieCommentListSerializer(comments)
    
    return Response(serialzer.data)

@api_view(['GET'])
def user_count(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    data = {
        'want_counts': user.user_wants.count(), #찜한영화
        'like_counts': user.moviecomment_set.count(), #평가한영화
        'followers_count': user.followers.count(),
        'followings_count': user.followings.count(),
    }
    return Response(data)

#####
## 유저 평점 기반 추천 알고리즘
@api_view(['GET'])
def user_recommend(request,username):
    user = get_object_or_404(get_user_model(), username=username)
    #rated_movie = user.user_wants.all()
    serializer = RecommendSerializer(user)
    
    return Response(serializer.data)






##################################################################
#temp

@api_view(["PUT",'GET'])
def temp(request, user_pk):

    user= get_object_or_404(get_user_model(), pk=user_pk)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)
        
    if request.method == "PUT":
        # user = get_object_or_404(get_user_model(),  pk=request.user.pk)
        serializer = UserSerializer(user, data= request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
