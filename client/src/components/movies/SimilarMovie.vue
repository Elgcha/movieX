<template>
  <div class='p-2 popular flex-6' @click="moveToDetail(movie.tmdb_id)">
      <img :src="imgSrc" alt="popularmovie" class="object-cover h-full">
      <div class="overlay">
      <h3 class="description">{{ movie.title }}</h3>
    </div>
  </div>
</template>

<script>
import {mapActions} from 'vuex'

export default {
  name: 'SimilarMovie',
  props: {
    movie: {
      type: Object,
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail',
    ])
  },
  computed: {
    imgSrc: function () {
      return 'https://image.tmdb.org/t/p/w500/' + this.movie.poster_path
    }
  },
}
</script>

<style>

</style>