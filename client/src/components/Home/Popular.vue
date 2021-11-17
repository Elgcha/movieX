<template>
  <div class="bg-dark">
    <popular-movies
    v-for="movie in movies"
    :key="movie.id"
    :movie="movie"
    >
    </popular-movies>
  </div>
</template>

<script>
import PopularMovies from '@/components/Home/PopularMovies.vue'
export default {
  components: { PopularMovies },
  name:'Popular',
  props: {
    movies: {
      type: Array,
    }
  }
}
</script>

<style>

</style>