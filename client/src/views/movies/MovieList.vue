<template>
  <div>
    <movie-search></movie-search>

    <!-- movielist -->
    <!-- <div v-if="movies[0]" class="flex flex-wrap">
      <div v-for="movie in movies" :key="movie.id" class='p-2 flex-6 popular' @click="moveToDetail(movie.id)">
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="popularmovie" class="object-cover h-full">
        <div class="overlay">
          <h3 class="description">{{ movie.title }}</h3>
        </div>
      </div>
    </div> -->
  </div>
</template>

<script>
import axios from 'axios'
import {mapActions} from 'vuex'
import MovieSearch from '../../components/movies/MovieSearch.vue'


export default {
  name: 'MovieList',
  components: {
    MovieSearch
  },
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
      const url = process.env.VUE_APP_URL + 'movies/'
      axios({
        methods: 'get',
        url: url
      })
        .then(res => {
          console.log(res)
          this.movies = res.data
          this.movies = this.movies.filter(movie => {
            return !movie.adult
          })
        })
    },
  },
  created: function () {
  }
}
</script>

<style>

</style>