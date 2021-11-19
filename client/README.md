# movieX-front

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

# 패치노트

## 11/18

* 게시판 기능 추가 - 글쓰기, 댓글 생성
* 메인페이지 인기 영화 목록 swiper 추가
* fuse.js를 통한 검색 기능 추가
* JWT 토큰을 통한 인증 추가

## 11/17

* 로그인, 회원가입 기능 추가
* 게시판 기능 추가 중
* 에러 시 뜨는 페이지 따로 생성
* 데이터 베이스 전체 영화 조회 페이지, 영화 상세페이지 생성
* 장고와 연결 - 데이터 가져오기
* fixtures 데이터 생성
* 혹시 모를 상황 대비해서 성인 영화 거르도록 filter 이용
* bootstrap -> tailwind css로 변경
* vue-awesome-swiper 추가
* 메인 페이지 carousel로 변경

## 11 / 16

* 기본모델 구성
* Face 컴포넌트 구성
  * 메인 이미지 가져오기 - 상영작 중 인기작
* 인기 영화 가져오기







# 문제점 & 해결

* 영화 카드에 마우스를 올리면 영화 제목이 뜨도록 하는 것

  css hover 속성 사용. translate를 사용하여 더 자연스럽게 작동하도록 구현. 나중에 더 수정해야할 필요는 있음

* actions에서 router 사용. 영화 디테일로 가는 method가 여러 곳에서 쓰이다 보니 vuex의 actions에서 처리하려고 했는데, 작동을 안한다....

  간단히 router를 import 해주니 해결되었다.

* 어떤 css 프레임워크를 사용해야 할지?

  bootstrap, tailwind, bootstrap-vue 중 고민 중

  

* 영화 목록 이미지 크기 똑같이 맞추기

  carousel을 추가하니 이미지 크기가 다시 달라져 버렸던 문제.. swiper 쪽에서 너비와 높이쪽을 건드려서 그런 듯.  object-fit: cover 가 작동을 안해서 한참 해멨는데, 찾아보니 이 설정은 너비와 높이 설정이 필요하다고 한다. 높이와 너비 100% 값을 줘서 해결.

