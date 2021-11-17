<template>
  <div>
    <div v-if="movies[0]">
      <div v-for="movie in movies" :key="movie.id" class='col-2 p-2 h-100 d-inline-block' @click="moveToDetail(movie.id)">
        <div v-if='movie' class='card popular'>
          <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="popularmovie" class="img-responsive img-rounded">
          <div class="overlay">
            <h3 class="description">{{ movie.title }}</h3>
          </div>
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