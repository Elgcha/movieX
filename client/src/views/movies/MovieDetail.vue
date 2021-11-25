<template>
  <div class="dark:text-white">
    <!-- moviesite 추가 -->
    <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"  role="alert" id="myAlert_moviesite">
      <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg top-20 w-96">
      <div class="mb-1">
        <label for="site" class="block mb-2 text-sm font-bold text-white">site </label>
        <input class="w-full px-3 py-2 leading-tight text-gray-700 bg-white border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="site" v-model="SiteData.site">
      </div>
      <div class="mb-1">
        <label for="link" class="block mb-2 text-sm font-bold text-white">link </label>
        <input @keyup.enter="login" class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 bg-white border rounded appearance-none hadow focus:outline-none focus:shadow-outline" type="text" id="link" v-model="SiteData.link" >
      </div>
      <div class="mb-1 ">
        <label for="price" class="block mb-2 text-sm font-bold text-white">price </label>
        <input class="w-full px-3 py-2 leading-tight text-gray-700 bg-white border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="price" v-model="SiteData.price">
      </div>
      <button @click="addMovieSite">Add</button>
      <span class="absolute inset-y-0 right-0 flex items-center mr-4" @click="alertClose">
        <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
      </span>
      </div>
    </div>
    <!-- moviesite 목록 -->
    <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-60"  role="alert" id="myAlert_moviesiteView">
      <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg opacity-90 top-20" style="width:50vw;">
      <span class="float-right mb-3" @click="alertClose">
        <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
      </span>
      <table class="w-full text-white rounded table-fixed bg-gradient-to-r from-gray-900 to-gray-800">
        <thead>
          <tr>
            <th class="w-4/12">site</th>
            <th class="w-6/12">link</th>
            <th class="w-1/12">price</th>
            <th class="w-1/12"></th>
          </tr>
        </thead>
      
        <tbody class="divide-y divide-gray-500 rounded">
          <tr v-for="site in movieSiteDatas" :key="site.id"  class="rounded hover:bg-gray-900">
            <td class="p-2 px-4 text-left rounded">{{ site.site }}</td>
            <td class="p-2 my-auto cursor-pointer" @click="move(site.link)">{{ site.link }}</td>
            <td class="p-2 rounded">{{ site.price }}</td>
            <td v-if="isAdmin" class="p-2 rounded cursor-pointer" @click="deleteMovieSite(site.id)">delete</td>
            <hr>
          </tr>
        </tbody>
      </table>
      <v-btn v-if="isAdmin" elevation="2" @click="alertOn" class="mt-10">add</v-btn>
      </div>
    </div>
    <!-- 메인 -->
    <div v-if="movie.title">
      <div class="w-full md:flex">
        <img :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : require('@/assets/images/default_poster.png')" alt="" class="p-3">
        <div class="w-full">
          <iframe class="w-full" :src="movieVideo" title="YouTube video player" frameborder="0" allowfullscreen id="my-iframe"></iframe>
          <div class="md:flex">
            <div class="px-2 py-1 text-2xl text-left">평점 : {{ movie.vote_average }}</div>
            <div class="p-2 py-1 my-auto text-2xl text-left">x-score: {{ userRate }}</div>
            <div class="my-5 ml-auto md:my-0">
              <v-btn elevation="2" class="" v-show="!wanted" @click='iWantThisMovie'>add want Movie</v-btn>
              <v-btn elevation="2" class="" v-show="wanted" @click='iWantThisMovie'>remove want Movie</v-btn>
            </div>
            <v-btn elevation="2" @click="alertViewOn" class="mb-3 ml-3 mr-4 md:mb-0">Link</v-btn>
          </div>
          <div class="pr-4">
            <div class="flex justify-between bg-gray-600 border-b">
              <h2 class="p-2 text-lg font-bold text-left">{{ movie.title }} <span class="text-sm text-gray-200">{{ movie.release_date }}</span></h2>
              <div class="p-2 my-auto">
                <span v-for="(genre, index) in movie.genres" :key="index" class="p-3 my-auto text-right">{{ genre.name }} </span>
              </div>
            </div>
            <p class="p-3 text-left bg-gray-700">{{ movie.overview }}</p>
          </div>
        </div>
      </div>
    </div>
    <h3 v-if="movie.people[0]" class="text-xl text-left">#출연</h3>
    <div v-swiper:mySwiper="swiperOption" class="my-2 swiper-container">
      <div class="swiper-wrapper">
        <div
        v-for="(people, index) in movie.people"
        :key="index"
        class="justify-center h-auto swiper-slide"
        @click="moveToPeopleDetail(people.id)"
        >
        <img :src="'https://image.tmdb.org/t/p/w500/' + people.profile_path" alt="" class="p-3 transform cursor-pointer hover:scale-105">
        {{ people.name }}
        </div>
      </div>
      <div class="swiper-button-prev" slot="button-prev"></div> 
      <div class="swiper-button-next" slot="button-next"></div>
    </div>
    
    <h3 class="p-1 text-xl text-left">#비슷한 영화</h3>
    <div v-swiper:mySwipers="swiperOption" class=" swiper-container">
      <div class="p-2 swiper-wrapper">
        <similar-movie 
        v-for="(similarMovie, index) in similarMovies"
        :key="index"
        :movie="similarMovie"
        class="justify-center h-auto swiper-slide"
        ></similar-movie>
      </div>
      <div class="swiper-button-prev" slot="button-prev"></div> 
      <div class="swiper-button-next" slot="button-next"></div>
    </div>
    <div>
      <comment :movie="movie" @changeOccur="getUserRate"></comment>
    </div>
  </div>
</template>

<script>
import Fuse from 'fuse.js'
import axios from 'axios'
import SimilarMovie from '@/components/movies/SimilarMovie.vue'
import Comment from '@/components/movies/Comment.vue'
import 'swiper/css/swiper.css'
import {mapActions} from 'vuex'

export default {
  components: { 
    SimilarMovie, 
    Comment 
  },
  name: 'MovieDetail',
  beforeRouteUpdate: function (to, from, next) {
    next()
    this.adminCheck()
    this.moviePk = this.$route.params.moviePk,
    this.getMovieDetail()
    this.getSimilarMovies()
    this.getUserRate()
    this.youWantIt()
    window.scrollTo(0,0)
  },
  data: function () {
    return {
      moviePk: this.$route.params.moviePk,
      movie: {},
      isAdmin: false,
      similarMovies: [],
      movieVideo: null,
      movieSiteDatas: {},
      swiperOption: {
        touchStartPreventDefault: false,
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        // autoplay: {
        //   delay:5000,
        // },
        breakpoints: {
          320: {
            slidesPerView: 2,
            spaceBetween: 20
          },
          480: {
            slidesPerView: 3,
            spaceBetween: 20
          },
          640: {
            slidesPerView: 4,
            spaceBetween: 20
          },
          1280: {
            slidesPerView: 6,
            spaceBetween: 20
          }
        },
        navigation: {
          nextEl: '.swiper-button-next', 
          prevEl: '.swiper-button-prev' 
        },
        observer: true,
        observeParents: true,
      },
      wanted: false,
      userRate: null,
      SiteData: {
        site: null,
        link: null,
        price: null,
      }
    }
  },
  computed: {
    imgSrc: function () {
      return 'https://image.tmdb.org/t/p/w500/' + this.movie.poster_path
    },
  },
  watch: {
    movie: function () {
      const key = process.env.VUE_APP_TMDB
      const url = `https://api.themoviedb.org/3/movie/${this.movie.tmdb_id}/videos`

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
      })
        .then(res => {
          return res.data.results
        })
        .then(data => {
          const option = {
            includeScore: true,
          // Search in `author` and in `tags` array
            keys: ['name']
          }
          const fuse = new Fuse(data, option)
          const result = fuse.search('메인 예고편')
          this.movieVideo = "https://www.youtube.com/embed/" + result[0].item.key
          
        })
    
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail',
    ]),
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getMovieDetail: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.movie = res.data
        })
    },
    getUserRate: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/rate/moviex/`
      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.userRate = res.data.score
        })
    },
    getSimilarMovies: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/same/`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.similarMovies = res.data
        })
    },
    iWantThisMovie: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/want/`
      axios({
        method: 'post',
        url: url,
        headers: this.setToken(),
      })
        .then(() => {
          this.wanted = !this.wanted
        })
        .catch(err => {
          console.log(err)
        })
    },
    adminCheck: function () {
      const url = process.env.VUE_APP_URL + `accounts/check/super/user/`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.isAdmin = res.data.use
        })
        .catch(err => {
          console.log(err)
        })
    },
    youWantIt: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/want/check/`
      axios({
        method: 'post',
        url: url,
        headers: this.setToken(),
      })
        .then((res) => {
          this.wanted = res.data.wanted
        })
        .catch(err => {
          console.log(err)
        })
    },
    heigthSize: function () {
      let iframe = document.querySelector("#iframe")
      iframe.style.height = iframe.contentDocument.body.scrollHeight + 'px'
      // iframe.style.width = iframe.contentDocument.body.scrollWidth + 'px'
    },
    moveToPeopleDetail: function(peoplePk) {
      this.$router.push({name:'PeopleDetail', params: {peoplePk: peoplePk}})
    },
    alertClose: function () {
      let alert = document.getElementById("myAlert_moviesite")
      let alert1 = document.getElementById("myAlert_moviesiteView")
      alert.style.display = "none"
      alert1.style.display = "none"
    },
    alertOn: function () {
      let alert = document.getElementById("myAlert_moviesiteView")
      alert.style.display = "none"
      let alert1 = document.getElementById("myAlert_moviesite")
      alert1.style.display = "block"
    },
    alertViewOn: function () {
      this.getMovieSite()
      let alert = document.getElementById("myAlert_moviesiteView")
      alert.style.display = "block"
    },
    addMovieSite: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/site/create/`
      axios({
        method: 'post',
        url: url,
        data: this.SiteData,
        headers: this.setToken(),
      })
        .then(() => {
          this.getMovieSite()
          let alert = document.getElementById("myAlert_moviesite")
          alert.style.display = "none"
          let alert1 = document.getElementById("myAlert_moviesiteView")
          alert1.style.display = "block"
          this.SiteData.site = null
          this.SiteData.link = null
          this.SiteData.price = null
        })
    },
    getMovieSite: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/site/view/`
      axios({
        method: 'get',
        url: url,
        data: this.SiteData,
        headers: this.setToken(),
      })
      .then(res => {
        this.movieSiteDatas = res.data
      })
    },
    deleteMovieSite: function (siteId) {
      const url = process.env.VUE_APP_URL + `movies/${this.moviePk}/site/delete/${siteId}/`
      axios({
        method: 'delete',
        url: url,
        data: this.SiteData,
        headers: this.setToken(),
      })
      .then(() => {
        this.getMovieSite()
      })
    },
    move: function(link){
      window.open(link)
    }
    
  },
  created: function () {
    this.adminCheck()
    this.getMovieDetail()
    this.getSimilarMovies()
    this.getUserRate()
    this.getMovieSite()
  },

}


</script>

<style>
#my-iframe { 
  display:block;
  border:none;
  height:50vh;
  width:50vw;
  padding: 2rem;
  
  }
</style>