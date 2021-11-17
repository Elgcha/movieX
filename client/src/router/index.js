import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Forum from '@/views/community/Forum.vue'
import Login from '@/views/accounts/Login.vue'
import Signup from '@/views/accounts/Signup.vue'
import ArticleCreate from '@/views/community/ArticleCreate.vue'
import err404 from '@/views/err/err404.vue'
import MovieList from '@/views/movies/MovieList.vue'
import MovieDetail from '@/views/movies/MovieDetail.vue'
import ArticleDetail from '@/views/community/ArticleDetail.vue'

Vue.use(VueRouter)

const routes = [
  // 메인 페이지
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  // 영화목록 페이지
  {
    path: '/movies/',
    name: 'MovieList',
    component: MovieList
  },
  {
    path: '/movies/:moviePk/',
    name: 'MovieDetail',
    component: MovieDetail
  },
  // 게시판 관련
  {
    path: '/community/forum/',
    name: 'Forum',
    component: Forum,
  },
  {
    path: '/community/forum/create/',
    name: 'ArticleCreate',
    component: ArticleCreate,
  },
  {
    path: '/community/forum/:articlePk/',
    name: 'ArticleDetail',
    component: ArticleDetail,
  },
  // accounts 관련
  {
    path: '/accounts/login/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/signup/',
    name: 'Signup',
    component: Signup,
  },
  // 에러페이지
  {
    path: '/404/',
    name: 'err404',
    component: err404,
  },

  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})



export default router
