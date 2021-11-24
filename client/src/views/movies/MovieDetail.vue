<template>
  <div class="dark:text-white">
    <div v-if="movie.title">
      <div class="flex w-full">
        <img :src="imgSrc" alt="" class="p-3">
        <div class="w-full">
          <iframe class="w-full" :src="movieVideo" title="YouTube video player" frameborder="0" allowfullscreen id="my-iframe"></iframe>
          <div class="flex">
            <div class="px-2 py-1 text-2xl text-left">평점 : {{ movie.vote_average }}</div>
            <div class="p-2 py-1 my-auto text-2xl text-left">x-score: {{ userRate }}</div>
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
    <h3 v-if="movie.people[0]" class="text-left">#출연</h3>
    <div v-swiper:mySwiper="swiperOption" class="my-2 bg-gray-600 swiper-container">
      <div class="swiper-wrapper">
        <div
        v-for="people in movie.people"
        :key="people.id"
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
    <div class="m-3">
      <button class="btn btn-blue" v-show="!wanted" @click='iWantThisMovie'>보고싶은 영화에 추가</button>
      <button class="btn btn-blue" v-show="wanted" @click='iWantThisMovie'>보고싶은 영화에서 제거</button>
    </div>
    <h3 class="p-1 text-left">#비슷한 영화</h3>
    <div v-swiper:mySwipers="swiperOption" class="my-2 bg-gray-600 swiper-container">
      <div class="swiper-wrapper">
        <similar-movie 
        v-for="similarMovie in similarMovies"
        :key="similarMovie.id"
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
    this.moviePk = this.$route.params.moviePk,
    this.getMovieDetail()
    this.getSimilarMovies()
    this.getUserRate()
  },
  data: function () {
    return {
      moviePk: this.$route.params.moviePk,
      movie: {},
      similarMovies: [],
      movieVideo: null,
      swiperOption: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        // autoplay: {
        //   delay:5000,
        // },
        navigation: {
          nextEl: '.swiper-button-next', 
          prevEl: '.swiper-button-prev' 
        },
      },
      wanted: false,
      userRate: null,
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
    }
    
  },
  created: function () {
    this.getMovieDetail()
    this.getSimilarMovies()
    this.getUserRate()
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