<template>
  <div class='w-full h-auto cursor-pointer popular'>
      <img :src="imgSrc" alt="popularmovie" class="w-full h-full transform rounded hover:scale-110" @click="moveToDetail(movie.id)">

  </div>
</template>

<script>
// import FaceMoviesSimilar from '@/components/Home/FaceMoviesSimilar.vue'
import { mapActions } from 'vuex'

export default {
  components: {  },
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