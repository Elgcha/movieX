<template>
  <div class="flex flex-wrap w-full">
    <div v-for="movie in pagenatedMovies" :key="movie.id" class='grid flex-1 grid-cols-2 gap-2 p-2 rounded cursor-pointer hover:border-gray-600 hover:bg-gray-800 md:flex-3 popular' @click="moveToDetail(movie.item.id)">
        <img :src="movie.item.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.item.poster_path : require('@/assets/images/default_poster.png')" alt="poster" class="object-cover h-full transform cursor-pointer hover:scale-105">
        <div class="mt-6 text-lg text-white">
          <p>{{ movie.item.title }}</p>
          <p class="mt-3 text-sm">{{ movie.item.release_date }}</p>
        </div>
      </div>
      <!-- 페이지네이션 -->
      <div class="relative w-full mx-auto mb-20">
        
      <div class="container absolute w-full mx-auto my-2" style="left:34vw">
        <ul class="flex w-full mx-auto">
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 rounded-l hover:bg-gray-500" :disabled="pageNum === 0" @click="prevPage">Prev</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum > 1" @click="pageNum=0">1</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600" v-if="pageNum > 1" >...</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum" @click="prevPage">{{ pageNum }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500">{{ pageNum + 1 }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum < pageCount - 1" @click="nextPage">{{ pageNum + 2 }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" >...</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum < pageCount - 2" @click="pageNum=pageCount-1">{{ pageCount }}</button></li>
            <li><button class="h-10 px-5 text-white border border-gray-600 rounded-r hover:bg-gray-500" :disabled="pageNum >= pageCount - 1" @click="nextPage">Next</button></li>
        </ul>
    </div>
      </div>
  </div>
</template>

<script>
import {mapActions} from 'vuex'
export default {
  name: 'MoviePage',
  data: function () {
    return {
      pageNum: 0
    }
  },
  props: {
    movies: {
      type: Array,
    },
    pageSize: {
      type: Number,
      required: false,
      default: 12
    },
  },
  methods: {
    ...mapActions([
      'moveToDetail'
    ]),
    nextPage: function () {
      this.pageNum += 1;
    },
    prevPage: function () {
      this.pageNum -= 1;
    },
  },
  computed: {
    pageCount: function() {
      let movieNum = this.movies.length
      let movieSize = this.pageSize
      let page = Math.floor((movieNum-1) / movieSize) + 1
      return page
    },
    pagenatedMovies: function () {
      const start = this.pageNum * this.pageSize
      const end = start + this.pageSize
      return this.movies.slice(start, end)
    }
  },
}
</script>

<style>

</style>