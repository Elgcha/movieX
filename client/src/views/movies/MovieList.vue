<template>
  <div>
    <div v-if="movies[0]" class="flex flex-wrap">
      <div v-for="movie in movies" :key="movie.id" class='p-2 flex-6 popular' @click="moveToDetail(movie.tmdb_id)">
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="popularmovie" class="object-cover h-full">
        <div class="overlay">
          <h3 class="description">{{ movie.title }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import {mapActions} from 'vuex'


export default {
  name: 'MovieList',
  data: function () {
    return {
      movies: [],
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail',
    ]),
    getMovies: function() {
      axios({
        methods: 'get',
        url: 'http://127.0.0.1:8000/movies/',
      })
        .then(res => {
          console.log(res)
          this.movies = res.data
          this.movies = this.movies.filter(movie => {
            return !movie.adult
          })
        })
    }
  },
  created: function () {
    this.getMovies()
  }
}
</script>

<style>

</style>