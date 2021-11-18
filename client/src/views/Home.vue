<template>
  <div class="home">
    <face :movies="playingMovie"></face>
    <h2>인기 있는 영화</h2>
    <popular :movies="popularMovie"></popular>
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
      popularMovie: [], // 인기 영화
      key: process.env.VUE_APP_TMDB,
    }
  },
  methods: {
    // 메인 이미지 영화 가져오기 - 상영 중인 것 중 가장 인기작
    getBestPlayingMovie: function () {
      const key = this.key
      const url = 'https://api.themoviedb.org/3/movie/now_playing'

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
      })
        .then(res => {
          this.playingMovie = res.data.results
        })
        .catch(err => {
          console.log(err)
        })
    },
    getPopularMovies: function () {
      const key = this.key
      const url = 'https://api.themoviedb.org/3/movie/popular'

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
      })
        .then(res => {
          this.popularMovie = res.data.results.slice(0, 6)
        })
    }
  },
  created: function () {
    this.getBestPlayingMovie()
    this.getPopularMovies()
  }
}
</script>
