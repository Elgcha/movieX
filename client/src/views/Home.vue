<template>
  <div class="dark:text-white home">
    <main-top></main-top>
    <div class="">

    <h2 class="mt-10 mb-2 text-lg text-left font-notosans">#인기 영화</h2>
    <div class="p-2">
      <popular :movies="newMovie"></popular>
    </div>
    <div>
    <h2 class="mt-10 mb-2 text-lg text-left font-notosans">#추천 영화</h2>
    </div>
    <div v-if="recommendMovies" class="p-2">
      <recommend :movies="recommendMovies"></recommend>
    </div>
    <div v-else><v-progress-circular
      indeterminate
      color="primary"
    ></v-progress-circular></div>
    <h2 class="mt-10 mb-2 text-lg text-left font-notosans">#{{ randomGenre }}</h2>
    <div>
      <face :movies="randomMovie"></face>
    </div>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Face from '@/components/Home/Face.vue'
import axios from 'axios'
import Popular from '@/components/Home/Popular.vue'
import Recommend from '../components/Home/Recommend.vue'
import MainTop from '@/components/Home/MainTop.vue'
import _ from 'lodash'


export default {

  name: 'Home',
  components: {
    Face,
    Popular,
    Recommend,
    MainTop
  },
  data: function () {
    return {
      randomMovie: [], // 랜덤 장르 영화
      newMovie: [], // 인기 영화
      key: process.env.VUE_APP_TMDB,
      recommendMovies: null,
      randomGenre: null,
      
      
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
    // 메인 이미지 영화 가져오기 
    getRandomMovie: function () {
      const genre = ['액션', '전쟁', '모험', '판타지', '애니메이션', '드라마', '공포', '코미디', '로맨스', '가족', 'SF']
      const nowGenre = _.sample(genre)
      this.randomGenre = nowGenre
      const url = process.env.VUE_APP_URL + `movies/${nowGenre}/`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.randomMovie = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    getNewMovies: function () {
      const url = process.env.VUE_APP_URL + 'movies/get/date/'

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.newMovie = res.data
        })
    },
    getRecommendMovie: function () {
      const username = localStorage.getItem('username')
      const url = process.env.VUE_APP_URL + `movies/${username}/test/recommend/`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.recommendMovies = res.data
        })
    }
  },
  created: function () {
    this.getRandomMovie()
    this.getNewMovies()
    this.getRecommendMovie()
  }
}
</script>
