<template>
  <div class="flex flex-wrap">
    <div v-for="movie in pagenatedMovies" :key="movie.id" class='grid grid-cols-2 gap-2 p-2 border flex-3 popular' @click="moveToDetail(movie.item.id)">
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.item.poster_path" alt="poster" class="object-cover h-full">
        <div class="text-white">
          <p>{{ movie.item.title }}</p>
          <p>{{ movie.item.release_date }}</p>
        </div>
      </div>
      <!-- 페이지네이션 -->
      <div class="container flex justify-center mx-auto my-2">
        <ul class="flex">
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 hover:bg-gray-100" :disabled="pageNum === 0" @click="prevPage">Prev</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 1" @click="pageNum=0">1</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 1" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum" @click="prevPage">{{ pageNum }}</button></li>
            <li><button class="h-10 px-5 text-white bg-gray-600 border border-r-0 border-gray-600 ">{{ pageNum + 1 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 hover:bg-gray-100" v-if="pageNum < pageCount - 1" @click="nextPage">{{ pageNum + 2 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" @click="pageNum=pageCount-1">{{ pageCount }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-gray-600 hover:bg-gray-100" :disabled="pageNum >= pageCount - 1" @click="nextPage">Next</button></li>
        </ul>
    </div>
  </div>
</template>

<script>
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