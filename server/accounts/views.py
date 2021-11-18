from django.shortcuts import get_object_or_404, render
from rest_framework import serializers, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.

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


#프로필 페이지 구성할거 가져오기
@api_view(['GET'])
def profile(request):
    user = get_object_or_404(get_user_model(), pk=request.user.pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)

# @api_view(['POST'])
# def profile2(request, user_pk):
#     user = get_object_or_404(get_user_model(), pk=user_pk)
#     serializer = UserSerializer(user)

#     return Response(serializer.data)

def follow(request, user_pk):
    #팔로우할 대상
    person = get_object_or_404(get_user_model(), pk= user_pk)
    #나
    user = request.user
    if person != user:
        if user.followers.filter(pk=person.pk).exist():
            person.followers.remove(user)
            isFollowed = False
        else:
            person.follwers.add(user)
            isFollowed = True
        context = {
            'isFollowed': isFollowed,
            'followers_count': person.followers.count(),
            'followings_count': person.followings.count(),
        }
        #JsonResponse로 리턴해야하는지?
        # return JsonResponse(context)
        return Response(context)

def login(request):
    pass

def update(request):
    pass

def delete(request):
    pass

def password_change(request):
    pass



