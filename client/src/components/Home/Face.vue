<template>
  <div v-swiper:mySwiper="swiperOption" class="my-2 swiper-container" id="face-container">
    <div class="p-2 swiper-wrapper">
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
        touchStartPreventDefault: false,
        slidesPerView: 6,
        spaceBetween: 10,
        // loop: true,
        // autoplay: {
        //   delay:5000,
        // },
        breakpoints: {
          320: {
            slidesPerView: 2,
            spaceBetween: 20
          },
          480: {
            slidesPerView: 3,
            spaceBetween: 30
          },
          640: {
            slidesPerView: 4,
            spaceBetween: 40
          },
          1280: {
            slidesPerView: 6,
            spaceBetween: 40
          }
        },
        navigation: {
          nextEl: '.swiper-button-next', 
          prevEl: '.swiper-button-prev' 
        },
      },
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