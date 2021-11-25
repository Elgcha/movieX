<template>
  <div class="hidden md:block">
    <!-- <div style="height:40vh;" class="z-0 overflow-hidden rounded ">
      <div class="relative z-0 overflow-hidden">
        <img :src="'https://image.tmdb.org/t/p/w500' + mainMovie.backdrop_path" alt="backdop" class="z-0 hidden md:block from-white bg-gradient-to-b to-black" style="width:100vw;">
      </div>
    </div> -->
    <div class="p-2">
    <div class="flex p-3 rounded-md">
      <div class="w-full my-auto">
        <img :src="'https://image.tmdb.org/t/p/w500' + mainMovie.poster_path" alt="" class="w-3/4 m-auto cursor-pointer" @click="moveToDetail(mainMovie.id)">
      </div>
      <div class="w-1/2 p-2 ">
        <div class="flex">
          <div class="text-3xl font-notosans">{{mainMovie.title}}</div>
          <div class="ml-auto mr-1 text-xl">{{mainMovie.vote_average}} </div>
          <span><svg class="block w-6 h-6 mt-auto text-yellow-400" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg></span>
        </div>
        <div class="">
          <div class="p-1 ml-3 text-sm text-left">개봉: {{ mainMovie.release_date}}</div>
          <div class="p-1 mt-10 text-2xl text-left border-b border-gray-400">줄거리</div>
          <div class="p-2 text-left">{{mainMovie.overview}}</div>
          <iframe v-if="movieVideo" class="w-full" :src="movieVideo" title="YouTube video player" frameborder="0" allowfullscreen id="my-iframe2"></iframe>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Fuse from 'fuse.js'
import _ from 'lodash'
import {mapActions} from 'vuex'

export default {
  name: 'MainTop',
  data: function () {
    return {
      mainMovie: {},
      movieVideo: null,
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail'
    ]),
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getRandomMovie: function () {
      const url = process.env.VUE_APP_URL + `movies/대문/`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.mainMovie = _.sample(res.data)
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created: function() {
    this.getRandomMovie()
  },
  watch: {
    mainMovie: function () {
      const key = process.env.VUE_APP_TMDB
      const url = `https://api.themoviedb.org/3/movie/${this.mainMovie.tmdb_id}/videos`

      axios({
        method: 'get',
        url: url,
        params: {
          api_key: key,
          language: 'ko-KR',
        }
      })
        .then(res => {
          return res.data.results
        })
        .then(data => {
          const option = {
            includeScore: true,
          // Search in `author` and in `tags` array
            keys: ['name']
          }
          const fuse = new Fuse(data, option)
          const result = fuse.search('예고편')
          this.movieVideo = "https://www.youtube.com/embed/" + result[0].item.key
          
        })
    
    },
  }
}
</script>

<style>
#my-iframe2 { 
  display:block;
  border:none;
  height:50vh;
  width:40vw;
  padding: 2rem;
  
  }
</style>