<template>
<div>
  <!-- 검색창 -->
  <div class="relative w-1/3 mx-auto mt-3">
    <div class="flex w-full">
      <input type="text" @input="inputChange" class="w-full py-2 text-gray-700 border rounded shadow appearance-none place-self-auto focus:outline-none focus:shadow-outline" id="search_input">
      <button @click="searchMovie" class="place-self-auto btn btn-blue btn-blue:hover"><img src="https://raw.githubusercontent.com/filippo-quacquarelli/tag-search/master/search.png" alt="search"></button>
    </div>
    <!-- 자동완성 -->

    <div class="absolute z-10 w-full text-left bg-white divide-y rounded-md" v-show="autosearch" tabindex="-1">
      <div v-for="autoMovie in autoCompleted" :key=autoMovie.score class="p-1 hover:bg-gray-300" @click="autoCompleteSearch(autoMovie.item.title)">
        {{ autoMovie.item.title }}
      </div>
    </div>
  </div>



  <!-- 영화 결과 출력부 -->
  <div v-if="isSearched" class="text-white">영화 검색 결과: {{ searchedMovie.length }}개</div>
  <div v-if="searchedMovie[0]" class="">  
    <movie-page :movies="searchedMovie"></movie-page>
    </div>

    <!-- 배우 결과 출력 -->
  <div v-if="isSearched" class="mt-3 text-white">배우 검색 결과: {{ searchedPeople.length }}명</div>
  <div v-if="searchedPeople[0]">
    <people-page :peoples="searchedPeople"></people-page>
  </div>

    <!-- 게시물 결과 출력 -->
  <div v-if="isSearched" class="mt-3 text-white">게시물 검색 결과: {{ searchedArticle.length }}개</div>
  <div v-if="searchedArticle[0]">
      <article-page :articles="searchedArticle"></article-page>
    </div>
</div>
</template>

<script>
import Fuse from 'fuse.js'
import axios from 'axios'
import {mapActions} from 'vuex'
import MoviePage from '../paginations/moviePage.vue'
import PeoplePage from '../paginations/peoplePage.vue'
import ArticlePage from '../paginations/articlePage.vue'

export default {
  name: 'MovieSearch',
  components: {
    MoviePage,
    PeoplePage,
    ArticlePage

  },
  data: function () {
    return {
      search: null,
      autosearch: true,
      autoCompleted: [],
      searchedMovie: [],
      searchedPeople: [],
      searchedArticle: [],
      movies: [],
      peoples: [],
      articles: [],
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
          this.movies = res.data
          this.movies = this.movies.filter(movie => {
            return !movie.adult
          })
        })
    },
    getPeople: function () {
      const url = process.env.VUE_APP_URL + 'movies/people/'
      axios({
        methods: 'get',
        url: url
      })
        .then(res => {
          this.peoples = res.data
        })
    },
    getArticles: function () {
      const url = process.env.VUE_APP_URL + 'community/'
      axios({
        methods: 'get',
        url: url
      })
        .then(res => {
          this.articles = res.data
        })
    },
    inputChange: function(event) {
      this.search = event.target.value.trim()
      if (this.search) {
        let num = 1
        if (this.search.length > 1) {
          num += 1
        }
        const options_movie = {
          includeScore: true,
          includeMatches: true,
          minMatchCharLength: num,
          // Search in `author` and in `tags` array
          keys: ['title', 'original_title']
        }
        const fuseMovie = new Fuse(this.movies, options_movie)
        const result = fuseMovie.search(this.search)
        this.autoCompleted = result.slice(0, 10)
      } else {
        this.autoCompleted = []
      }
    },
    searchMovie: function () {
      this.autoCompleted = []
      // 한글자 검색시 생각
      let num = 1
      if (this.search.length > 1) {
        num += 1
      }
      const options_movie = {
        includeScore: true,
        includeMatches: true,
        minMatchCharLength: num,
        // Search in `author` and in `tags` array
        keys: ['title', 'original_title', 'genres.name']
      }
      const options_people = {
        includeScore: true,
        includeMatches: true,
        minMatchCharLength: num,
        // Search in `author` and in `tags` array
        keys: ['name', 'also_known_as', 'movie_title.title']
      }
      const options_article = {
        includeScore: true,
        includeMatches: true,
        minMatchCharLength: num,
        keys: ['title', 'content']
      }
      const fuseMovie = new Fuse(this.movies, options_movie)
      const fusePeople = new Fuse(this.peoples, options_people)
      const fuseArticle = new Fuse(this.articles, options_article)
      const result = fuseMovie.search(this.search)
      const result1 = fusePeople.search(this.search)
      const result2 = fuseArticle.search(this.search)
      this.searchedMovie = result
      this.searchedPeople = result1
      this.searchedArticle = result2
      this.isSearched = true
      const searchInput = document.querySelector('#search_input')
      searchInput.value = this.search

    },
    autoCompleteSearch: function (title) {
      this.search = title
      this.searchMovie()
    },

  },
  created: function() {
    this.getMovies()
    this.getPeople()
    this.getArticles()
  }
}
</script>

<style>

</style>