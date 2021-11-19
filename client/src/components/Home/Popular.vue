<template>
<div v-swiper:mySwiper="swiperOption" class="my-2 swiper-container">
  <div class="bg-dark swiper-wrapper">
    <popular-movies
    v-for="movie in movies"
    :key="movie.id"
    :movie="movie"
    class="justify-center h-auto swiper-slide"
    >
    </popular-movies>
  </div>
  <div class="swiper-button-prev" slot="button-prev"></div> 
  <div class="swiper-button-next" slot="button-next"></div>


</div>
</template>

<script>
import PopularMovies from '@/components/Home/PopularMovies.vue'
import 'swiper/css/swiper.css'

export default {
  components: { PopularMovies },
  name:'Popular',
  data: function () {
    return {
      swiperOption: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: true,
        // autoplay: {
        //   delay:5000,
        // },
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