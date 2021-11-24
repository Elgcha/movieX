<template>
  <div class="dark:text-white home">
    <h2 class="mt-10 mb-2 text-left">#인기 영화</h2>
    <div class="p-2 dark:bg-gray-600">
      <popular :movies="newMovie"></popular>
    </div>
    <div>
    <h2 class="mt-10 mb-2 text-left">#추천 영화</h2>
    </div>
    <div class="p-2 dark:bg-gray-500">
      <recommend :movies="recommendMovies"></recommend>
    </div>
    <h2>{{ randomGenre }}</h2>
    <div>
      <face :movies="randomMovie"></face>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Face from '@/components/Home/Face.vue'
import axios from 'axios'
import Popular from '@/components/Home/Popular.vue'
import Recommend from '../components/Home/Recommend.vue'
import _ from 'lodash'


export default {

  name: 'Home',
  components: {
    Face,
    Popular,
    Recommend,
  },
  data: function () {
    return {
      randomMovie: [], // 랜덤 장르 영화
      newMovie: [], // 인기 영화
      key: process.env.VUE_APP_TMDB,
      recommendMovies: [],
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
