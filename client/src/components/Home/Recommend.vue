<template>
<div v-swiper:mySwiper="swiperOption" class="my-2 swiper-container">
  <div class="p-2 swiper-wrapper">
    <recommend-movies
    v-for="movie in movies"
    :key="movie.id"
    :movie="movie"
    class="justify-center h-auto swiper-slide"
    >
    </recommend-movies>
  </div>
  <div class="swiper-button-prev" slot="button-prev"></div> 
  <div class="swiper-button-next" slot="button-next"></div>


</div>
</template>

<script>

import 'swiper/css/swiper.css'
import RecommendMovies from './RecommendMovies.vue'

export default {
  components: {RecommendMovies  },
  name:'Recommend',
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
  }
}
</script>

<style>

</style>