<template>
  <div class="text-white">
    <div class="flex p-3">
      <img :src="'https://image.tmdb.org/t/p/w500/' + people.profile_path" alt="" class="w-1/4 p-3 mt-2">
      <div>
        <div class="p-3">{{ people.name }}</div>
        <div v-if="people.gender === 1">여</div>
        <div v-else>남</div>
      </div>
    </div>
    <!-- 슬라이드 -->
    <h3>출연</h3>
    <div v-swiper:mySwiper="swiperOption1" class="my-2 bg-gray-600 swiper-container">
      <div class="swiper-wrapper">
        <div
        v-for="movie in people.movie_title"
        :key="movie.id"
        class="justify-center h-auto swiper-slide"
        @click="moveToDetail(movie.id)"
        >
        <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="" class="p-3">
        {{ movie.title }}
        </div>
      </div>
      <div class="swiper-button-prev1" slot="button-prev"></div> 
      <div class="swiper-button-next1" slot="button-next"></div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
import axios from 'axios'
export default {
  name: 'PeopleDetail',
  data: function () {
    return {
      people: {},
      swiperOption1: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        // autoplay: {
        //   delay:5000,
        // },
        navigation: {
          nextEl: '.swiper-button-next1', 
          prevEl: '.swiper-button-prev1' 
        },
      },
    }
  },
  methods: {
    ...mapActions([
      'moveToDetail',
    ]),
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getPeople: function () {
      const url = process.env.VUE_APP_URL + `movies/people/${this.$route.params.peoplePk}`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.people = res.data
        })
    },
  },
  created: function () {
    this.getPeople()
  },
  computed: {
    
  }
}
</script>

<style>

</style>