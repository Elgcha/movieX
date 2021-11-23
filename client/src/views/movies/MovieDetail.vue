<template>
  <div class="dark:text-white">
    <div v-if="movie.title">
      <div class="flex w-full">
        <img :src="imgSrc" alt="" class="p-3">
        <div class="w-full">
          <iframe class="w-full" :src="movieVideo" title="YouTube video player" frameborder="0" allowfullscreen id="my-iframe"></iframe>
          <div class="p-2 text-2xl text-left">평점 : {{ movie.vote_average }}</div>
          <div class="flex justify-between bg-gray-600 border-b">
            <h2 class="p-2 text-left ">{{ movie.title }} {{ movie.release_date }}</h2>
            <div class="p-2">
              <span v-for="genre in movie.genres" :key="genre" class="p-3 text-right">{{ genre.name }} </span>
            </div>
          </div>
          <p class="p-3 text-left bg-gray-700">{{ movie.overview }}</p>
        </div>
      </div>
    </div>
    <h3>출연</h3>
    <div v-swiper:mySwiper="swiperOption1" class="my-2 bg-gray-600 swiper-container">
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
      <div class="swiper-button-prev1" slot="button-prev"></div> 
      <div class="swiper-button-next1" slot="button-next"></div>
    </div>
    <div class="m-3">
      <button v-show="!wanted" @click='iWantThisMovie'>보고싶은 영화에 추가</button>
      <button v-show="wanted" @click='iWantThisMovie'>보고싶은 영화에서 제거</button>
    </div>
    <h3>비슷한 영화</h3>
    <div v-swiper:mySwiper="swiperOption" class="my-2 bg-gray-600 swiper-container">
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
      <comment :movie="movie"></comment>
    </div>
  </div>
</template>

<script>
import Fuse from 'fuse.js'
import axios from 'axios'
import SimilarMovie from '@/components/movies/SimilarMovie.vue'
import Comment from '@/components/movies/Comment.vue'
import 'swiper/css/swiper.css'

export default {
  components: { 
    SimilarMovie, 
    Comment 
  },
  name: 'MovieDetail',
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
      swiperOption1: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        // autoplay: {
        //   delay:5000,
        // },
        navigation: {
          nextEl: '.swiper-button-next1', 
          prevEl: '.swiper-button-prev1' 
        },
      },
      wanted: false,
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
    getSimilarMovies: function () {
      const key = process.env.VUE_APP_TMDB
      const url = `https://api.themoviedb.org/3/movie/${this.moviePk}/similar`

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
      })
        .then(res => {
          this.similarMovies = res.data.results
          this.similarMovies = this.similarMovies.filter(movie => {
            return !movie.adult
          })
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