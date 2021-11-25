<template>
  <div>
    <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"  role="alert" id="myAlert2">
      <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg bg-opacity-90 top-20 w-96">
      <div>{{errMessage}}</div>
      <span class="absolute inset-y-0 right-0 flex items-center mr-4" @click="alertClose">
        <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
      </span>
      </div>
    </div>
    <!-- 검색 -->
    <div class="flex">

    <div class="flex w-1/3 mx-auto my-3">
      <v-icon>fas fa-search</v-icon>
      <v-text-field dark clearable label="Movie" @input="inputChange($event)" @keyup.enter="searchMovie"></v-text-field>
      <!-- <input type="text" @input="inputChange" @keyup.enter="searchMovie" class="w-full py-2 text-gray-700 border rounded shadow place-self-auto focus:outline-none focus:shadow-outline" id="search_input"> -->
      <!-- <button @click="searchMovie" class="place-self-auto btn btn-blue btn-blue:hover"><img src="https://raw.githubusercontent.com/filippo-quacquarelli/tag-search/master/search.png" alt="search"></button> -->
    </div>
    <div class="flex">
      <v-btn class="mx-1 ml-auto text-black cursor-pointer" @click="allMovieUpdate">Update</v-btn>
      <v-btn class="mx-1 text-black cursor-pointer" @click="peopleMovieConnect">Connect</v-btn>
    </div>
    </div>
    
    <!-- 출력 -->
    <div class="flex flex-wrap">
      <div v-for="movie in searchedMovies" :key="movie.id" @click="addMovie(movie.id)" class='grid flex-1 grid-cols-2 gap-2 p-2 rounded cursor-pointer hover:border-gray-600 hover:bg-gray-800 md:flex-3 popular'>
        <img :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : require('@/assets/images/default_poster.png')" alt="poster" class="object-cover h-full transform cursor-pointer hover:scale-105">
        <div class="mt-6 text-lg text-white">
          <p>{{ movie.title }}</p>
          <p class="text-sm">{{ movie.release_date }}</p>
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
      errMessage: null,
    }
  },
  methods: {
    alertClose: function () {
      let alert = document.getElementById("myAlert2")
      alert.style.display = "none"
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    inputChange: function (event) {
      this.search = event
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
      const url = process.env.VUE_APP_URL + `movies/search/${tmdbId}/`
      // const url2 = process.env.VUE_APP_URL + 'movies/connect/mtop/'
      axios({
        method: 'post',
        url: url,
        headers: this.setToken()
      })
        .then((res) => {
          if (res.data.message) {
            this.errMessage = res.data.message
            let alert = document.getElementById("myAlert2")
            alert.style.display = "block"
          } else {
            this.errMessage = '추가되었습니다.'
            let alert = document.getElementById("myAlert2")
            alert.style.display = "block"
            // axios({
            //   method: 'get',
            //   url: url2,
            // })
          }
        })
        .catch(err => {
          console.log(err)
        })
    },
    peopleMovieConnect: function () {
      const url = process.env.VUE_APP_URL + 'movies/connect/mtop/'
      axios({
        method: 'get',
        url: url,
      })
        .then(() => {
          this.errMessage = '완료되었습니다.'
          let alert = document.getElementById("myAlert2")
          alert.style.display = "block"
        })
    },
    allMovieUpdate: function () {
      const url = process.env.VUE_APP_URL + 'movies/update/movies/all/' 
      axios({
        method: 'get',
        url: url,
      })
      .then(() => {
          this.errMessage = '완료되었습니다.'
          let alert = document.getElementById("myAlert2")
          alert.style.display = "block"
        })
    },
  }
}
</script>

<style>

</style>