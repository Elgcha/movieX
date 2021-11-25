from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .serializers import MovieCommentListSerializer, RecommendSerializer, UserSerializer
# Create your views here.

#### user #####################################
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    # Client에서 데이터 받아오기
    password = request.data.get('password')
    passwordConfirmation = request.data.get('passwordConfirmation')
    username = request.data.get('username')
    email = request.data.get('email')
    # 일치여부 확인
    try:
        if password != passwordConfirmation:
            return Response({ 'error': '비밀번호가 일치하지 않습니다.'})
        UserModel = get_user_model()
        person = UserModel.objects.filter(username=username)
        if person:
            return Response({ 'error': '이미 존재하는 닉네임입니다.'})
        # UserSerializer를 통해 데이터 직렬화
        if  email != '@' not in email or not (email[-4:] == '.com') :
            return Response({ 'error': '잘못된 이메일 형식입니다.'})
        serializer = UserSerializer(data=request.data)
    
        #validation 작업 진행 -> password도 같이 직렬화 진행
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            #비밀번호 해싱 후 
            user.set_password(request.data.get('password'))
            user.save()
            # password는 직렬화 과정에는 포함 되지만 → 표현(response)할 때는 나타나지 않는다.
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    except TypeError:
        return Response({ "error": '입력하지 않은 칸이 있습니다.'})


#####################프로필 페이지 구성할거 가져오기 
@api_view(['GET'])
def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = UserSerializer(user)
    return Response(serializer.data)
#############################################
@api_view(['GET'])
def profile_self(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    serializer = UserSerializer(user)
    return Response(serializer.data)

@api_view(['POST'])
def follow(request, username):
    #팔로우할 대상
    person = get_object_or_404(get_user_model(), username=username)
     
    #나
    user = request.user
    if person != user:
        if person.followers.filter(pk=user.pk).exists():
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
        print(data)
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
    #### 팔로우 리스트, 팔로잉 리스트 목록
@api_view(['GET'])
def follow_list(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    followings = user.followings.all()
    followers = user.followers.all()
    wings_list = []
    er_list = []
    for a in followings:
        wings_list.append(a.username)
    for b in followers:
        er_list.append(b.username)
        
    data = {
        'followings': wings_list,
        'followers': er_list,
    }
    return Response(data)

#####
## 유저가 평가한 영화목록을 보여주는데
@api_view(['GET'])
def user_recommend(request,username):
    user = get_object_or_404(get_user_model(), username=username)
    serializer = RecommendSerializer(user)
    
    return Response(serializer.data)

@api_view(["PUT",'GET'])
# @permission_classes([AllowAny])
def image(request, username):

    user= get_object_or_404(get_user_model(), username=username)

    if request.method == "GET":
        data = user.image_path
        return Response(data)
        
    if request.method == "PUT":
        src = request.data['image']
        user.image_path = src
        user.save()
        return Response(status=status.HTTP_200_OK)

@api_view(["PUT"])
def email_change(request, username):
    users = get_user_model()
    person = get_object_or_404(users, username=username)
    email = request.data.get('email')
    if '@' not in email or not (email[-4:] == '.com'):
         return Response({ 'error': '잘못된 이메일 형식입니다.'})
    person.email = email
    person.save()
    return Response(status=status.HTTP_200_OK)