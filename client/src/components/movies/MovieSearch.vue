<template>
<div>
  <!-- 검색창 -->
  <div class="my-3">
    <input type="text" @input="inputChange">
    <button @click="searchMovie" class="mx-2 btn btn-blue btn-blue:hover">search</button>
  </div>

  <!-- 영화 결과 출력부 -->
  <div v-if="isSearched" class="text-white">영화 검색 결과: {{ searched.length }}개</div>
  <div v-if="searched[0]" class="flex flex-wrap gap-2">
      <div v-for="movie in searched" :key="movie.id" class='grid grid-cols-2 gap-2 p-2 border flex-3 popular' @click="moveToDetail(movie.item.id)">
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.item.poster_path" alt="poster" class="object-cover h-full">
        <div class="text-white">
          <p>{{ movie.item.title }}</p>
          <p>{{ movie.item.release_date }}</p>
        </div>
        
      </div>
    </div>

    <!-- 배우 결과 출력 -->

    <!-- 게시물 결과 출력 -->
</div>
</template>

<script>
import Fuse from 'fuse.js'
import axios from 'axios'
import {mapActions} from 'vuex'

export default {
  name: 'MovieSearch',
  data: function () {
    return {
      search: null,
      searched: [],
      movies: [],
      isSearched: false,
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail'
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
    inputChange: function(event) {
      this.search = event.target.value
    },
    searchMovie: function () {
      const options = {
        includeScore: true,
        // Search in `author` and in `tags` array
        keys: ['title', 'original_title']
      }
      const fuse = new Fuse(this.movies, options)
      const result = fuse.search(this.search)
      this.searched = result
      this.isSearched = true

    },

  },
  created: function() {
    this.getMovies()
  }
}
</script>

<style>

</style>