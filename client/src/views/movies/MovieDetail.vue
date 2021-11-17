<template>
  <div>

  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'MovieDetail',
  data: function () {
    return {
      moviePk: this.$route.params.moviePk,
      movie: {},
    }
  },
  computed: {
    imgSrc: function () {
      return 'https://image.tmdb.org/t/p/w500/' + this.movie.backdrop_path
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
          console.log(res)
        })

    },
  },
  created: function () {
    this.getMovieDetail()
  }

}
</script>

<style>

</style>