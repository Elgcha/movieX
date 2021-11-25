<template>
  <div class="text-white">
    <div class="flex p-3">
      <img :src="'https://image.tmdb.org/t/p/w500/' + people.profile_path" alt="" class="w-1/4 p-3 mt-2">
      <div class="text-left">
        <div class="p-3 text-2xl">{{ people.name }}</div>
        <div class="p-3">{{ people.birthday }}</div>
        <div class="p-3">{{ people.known_for_department }}</div>
      </div>
        <img :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : require('@/assets/images/default_poster.png')" alt="" class="z-0 w-1/4 ml-auto opacity-70">
    </div>
    <!-- 슬라이드 -->
    <h3 class="text-left">#출연</h3>
    <div v-swiper:mySwiper="swiperOption1" class="my-2 swiper-container">
      <div class="p-2 swiper-wrapper">
        <div
        v-for="movie in people.movie_title"
        :key="movie.id"
        class="justify-center h-auto swiper-slide"
        @click="moveToDetail(movie.id)"
        >
        <img :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : require('@/assets/images/default_poster.png')" alt="" class="p-3 transform hover:scale-105">
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
import _ from 'lodash'
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
    movie: function () {
      return _.sample(this.people.movie_title)
    }
  }
}
</script>

<style>

</style>