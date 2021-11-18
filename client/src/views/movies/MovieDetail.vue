<template>
  <div>
    <div v-if="movie.title">
      <img :src="imgSrc" alt="">
      <p>{{ movie.title }}</p>
      <p>{{ movie.overview }}</p>
      <p>{{ movie.release_date }}</p>
    </div>
    <div>
      <button>평가하기</button>
      <button>코멘트 작성</button>
      <button>보고싶어요</button>
    </div>
    <div>
      <h3>비슷한 영화</h3>
      <div class="flex flex-wrap">
        <similar-movie 
        v-for="similarMovie in similarMovies"
        :key="similarMovie.id"
        :movie="similarMovie"
        class=""
        ></similar-movie>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import SimilarMovie from '@/components/movies/SimilarMovie.vue'

export default {
  components: { SimilarMovie },
  name: 'MovieDetail',
  data: function () {
    return {
      moviePk: this.$route.params.moviePk,
      movie: {},
      similarMovies: [],
    }
  },
  computed: {
    imgSrc: function () {
      return 'https://image.tmdb.org/t/p/w500/' + this.movie.poster_path
    }
  },
  methods: {
    getMovieDetail: function () {
      const key = process.env.VUE_APP_TMDB
      const url = `https://api.themoviedb.org/3/movie/${this.moviePk}`

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
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
    }
  },
  created: function () {
    this.getMovieDetail()
    this.getSimilarMovies()
  },

}
</script>

<style>

</style>