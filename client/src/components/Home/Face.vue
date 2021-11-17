<template>
  <div>
    <face-movies :movie="movie"></face-movies>
  </div>
</template>

<script>
import FaceMovies from '@/components/Home/FaceMovies.vue'
export default {
  components: { FaceMovies },
  name:'Face',
  props: {
    movie: {
      type: Object,
    }
  },
  methods: {
    
  },
}
</script>

<style>

</style>