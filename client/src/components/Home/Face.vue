<template>
  <div v-swiper:mySwiper="swiperOption" class="swiper-container" id="face-container">
    <div class="swiper-wrapper">
      <face-movies v-for="movie in movies" :key="movie.id" :movie="movie" class="cursor-pointer swiper-slide"></face-movies>
    </div>
  </div>
</template>

<script>
import FaceMovies from '@/components/Home/FaceMovies.vue'
import 'swiper/css/swiper.css'

export default {
  components: { FaceMovies },
  name:'Face',
  data: function () {
    return {
      swiperOption: {
        loop: true,
        autoplay: {
          delay:5000,
        },
      }
    }
  },
  props: {
    movies: {
      type: Array,
    }
  },
  methods: {
    
  },
  // mounted() {
  //     console.log('Current Swiper instance object', this.mySwiper)
  //     this.mySwiper.slideTo(3, 1000, false)
  //   }
}

</script>

<style>

</style>