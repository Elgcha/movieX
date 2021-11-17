<template>
  <div class='col-2 p-2 h-100 d-inline-block' @click="moveToDetail(movie.id)">
    <div v-if='movie' class='card popular'>
      <img :src="imgSrc" alt="popularmovie" class="img-responsive img-rounded">
      <div class="overlay">
        <h3 class="description">{{ movie.title }}</h3>
      </div>
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