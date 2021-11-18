<template>
  <div class="flex bg-dark">
    <popular-movies
    v-for="movie in movies"
    :key="movie.id"
    :movie="movie"
    class="h-100"
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