<template>
  <div class='w-full h-auto cursor-pointer popular'>
      <img :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : require('@/assets/images/default_poster.png')" alt="popularmovie" class="w-full h-full transform rounded hover:scale-110" @click="moveToDetail(movie.id)">

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
    
  },
}
</script>

<style>


</style>