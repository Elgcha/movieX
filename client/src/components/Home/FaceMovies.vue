<template>
  <div id="face" @click="moveToDetail(movie.id)">
    <img :src="imgSrc" alt="" v-if="movie" class='w-full rounded'  >
    <span v-if='movie' class="title">
      <p>{{ movie.title }}</p>
      </span>
    <span>
      <face-movies-similar :movie="movie"></face-movies-similar>
    </span>
  </div>
</template>

<script>
import FaceMoviesSimilar from '@/components/Home/FaceMoviesSimilar.vue'
import { mapActions } from 'vuex'

export default {
  components: { FaceMoviesSimilar },
  name:'FaceMovies',
  props: {
    movie: {
      type: Object,
    }
  },
  filters: {
    truncate: function(data, num){
        const reqdString = 
          data.slice(0, num)
        return reqdString +'...';
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