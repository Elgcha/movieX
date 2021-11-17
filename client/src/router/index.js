import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'
import Forum from '@/views/community/Forum.vue'
import Login from '@/views/accounts/Login.vue'
import Signup from '@/views/accounts/Signup.vue'
import ArticleCreate from '@/views/community/ArticleCreate.vue'
import err404 from '@/views/err/err404.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
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
    path: '/accounts/login/',
    name: 'Login',
    component: Login,
  },
  {
    path: '/accounts/signup/',
    name: 'Signup',
    component: Signup,
  },
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
