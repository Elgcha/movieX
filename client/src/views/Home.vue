<template>
  <div class="dark:text-white home">
    <face :movies="playingMovie"></face>
    <h2>인기 영화</h2>
    <div>
      <popular :movies="newMovie"></popular>
    </div>
  </div>
</template>

<script>
// @ is an alias to /src
import Face from '@/components/Home/Face.vue'
import axios from 'axios'
import Popular from '@/components/Home/Popular.vue'


export default {
  name: 'Home',
  components: {
    Face,
    Popular,
  },
  data: function () {
    return {
      playingMovie: [], // 상영 중 영화
      newMovie: [], // 인기 영화
      key: process.env.VUE_APP_TMDB,
      
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
    getBestPlayingMovie: function () {
      const url = process.env.VUE_APP_URL + 'movies/대문/'

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.playingMovie = res.data
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
    }
  },
  created: function () {
    this.getBestPlayingMovie()
    this.getNewMovies()
  }
}
</script>
