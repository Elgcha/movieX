<template>
  <div>
    <!-- 검색 -->
    <div class="flex w-1/3 mx-auto my-3">
      <input type="text" @input="inputChange" @keyup.enter="searchMovie" class="w-full py-2 text-gray-700 border rounded shadow appearance-none place-self-auto focus:outline-none focus:shadow-outline" id="search_input">
      <button @click="searchMovie" class="place-self-auto btn btn-blue btn-blue:hover"><img src="https://raw.githubusercontent.com/filippo-quacquarelli/tag-search/master/search.png" alt="search"></button>
    </div>
    
    <!-- 출력 -->
    <div class="flex flex-wrap">
      <div v-for="movie in searchedMovies" :key="movie.id" @click="addMovie(movie.id)" class='grid flex-1 grid-cols-2 gap-2 p-2 bg-gray-700 border border-gray-500 rounded cursor-pointer hover:border-gray-600 hover:bg-gray-600 md:flex-3 popular'>
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="poster" class="object-cover h-full transform cursor-pointer hover:scale-105">
        <div class="text-white">
          <p>{{ movie.title }}</p>
          <p>{{ movie.release_date }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MovieAdd',
  data: function () {
    return {
      search: null,
      searchedMovies: [],
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
    inputChange: function (event) {
      this.search = event.target.value
    },
    // tmdb 검색
    searchMovie: function () {
      const key = process.env.VUE_APP_TMDB
      const url = `https://api.themoviedb.org/3/search/movie`
      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
          include_adult: false,
          query: this.search,
        }
      })
        .then(res => {
          this.searchedMovies = res.data.results
        })
        .catch(err => {
          console.log(err)
        })
    },
    // db에 추가
    addMovie: function (tmdbId) {
      const url = process.env.VUE_APP_URL + `movies/create/${tmdbId}/`
      axios({
        method: 'post',
        url: url
      })
        .then(() => {
          
        })
        .catch(err => {
          console.log(err)
        })
    },
  }
}
</script>

<style>

</style>