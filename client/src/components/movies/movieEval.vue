<template>
<div class="">
  <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"  role="alert" id="myAlert">
    <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg top-20 w-96">
    <div>모든 영화를 평가하셨습니다.</div>
    <span class="absolute inset-y-0 right-0 flex items-center mr-4" @click="alertClose">
      <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
    </span>
    </div>
  </div>



  <button class="hidden mx-3 my-auto text-white md:block hover:text-gray-50" type="button" data-modal-toggle="movieEval" @click="toggle" id="movieModal">
    영화평가
  </button>
  <button class="px-2 mx-3 my-auto text-white md:hidden hover:text-gray-50" type="button" data-modal-toggle="movieEval" @click="toggle" id="movieModal">
    E
  </button>

  <!-- Main modal -->
  <transition
        enter-active-class="transition duration-100 ease-out"
        enter-class="transform scale-95 opacity-0"
        enter-to-class="transform scale-100 opacity-100"
        leave-active-class="transition duration-75 ease-in"
        leave-class="transform scale-100 opacity-100"
        leave-to-class="transform scale-95 opacity-0"
      >
  <div
    class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"
    id="my-modal"
  >
  <div
    v-if="movie"
    class="relative mx-auto border rounded-md shadow-lg top-20 w-96"
  >
    <v-card
    class="w-full mx-auto border-none"
    dark
  >
    <v-img
      :src="movie.poster_path ? 'https://image.tmdb.org/t/p/w500/' + movie.poster_path : '@/assets/images/default_poster.png'"
      class="h-full"
    ></v-img>

    <v-card-title>
      {{movie.title}}
    </v-card-title>

    <v-card-subtitle>
      {{movie.release_date}}
      <div class="flex">
        <star-rating v-model="rate"></star-rating>
        <v-btn elevation="2" class="ml-auto mr-1 " @click="createComment">next</v-btn>
        <v-btn elevation="2" class="mx-1 ml-auto " @click="getMovie">pass</v-btn>
      </div>
      <v-btn
          id="ok-btn"
          elevation="2"
          color="secondary"
          @click="endModal"
          class="w-1/2 px-4 py-2 my-2 text-base font-medium"
        >
          End
        </v-btn>
    </v-card-subtitle>

    <v-card-actions>
      <v-btn
        color="orange lighten-2"
        text
      >
        detail
      </v-btn>

      <v-spacer></v-spacer>

      <v-btn
        icon
        @click="show = !show"
      >
        <v-icon>{{ show ? 'mdi-chevron-up' : 'mdi-chevron-down' }}</v-icon>
      </v-btn>
    </v-card-actions>

    <v-expand-transition>
      <div v-show="show">
        <v-divider></v-divider>

        <v-card-text class="text-left">
          <div class="flex justify-center">
            <div v-for="(genre, index) in movie.genres" :key="index" class="mx-2 my-1"> {{ genre.name }} </div>
          </div>
         <span v-if="movie.overview">{{movie.overview}}</span>
         <span v-else> 이 영화는 줄거리가 제공되지 않습니다.</span>
        </v-card-text>
      </div>
    </v-expand-transition>
  </v-card>
    
    <!-- <div class="grid mt-3 text-center">
      <div>
        <div>
          <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="poster" class="p-1">
        </div>
        <div>
          <h3 class="mt-2 text-lg font-medium leading-6">{{movie.title}}</h3>
          <div class="flex justify-center">
            <div v-for="(genre, index) in movie.genres" :key="index" class="mx-2"> {{ genre.name }} </div>
          </div>
        </div>
      </div>
      <div class="flex">
        <star-rating v-model="rate"></star-rating>
        <button class="ml-auto btn btn-blue" @click="createComment">next</button>
        <button class="ml-auto btn btn-blue" @click="getMovie">pass</button>
      </div>
      <div class="items-center px-4 py-3">
        <button
          id="ok-btn"
          @click="endModal"
          class="w-1/2 px-4 py-2 text-base font-medium text-white bg-green-500 rounded-md shadow-sm hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-green-300"
        >
          End
        </button>
      </div>
    </div> -->
  </div>
  </div>
  </transition>


</div>
</template>

<script>
import axios from 'axios'
import starRating from '../ratings/starRating.vue'
export default {
  components: { starRating },
  name:'movieEval',
  data: function () {
    return {
      movie: null,
      show: false,
      rate: 3,

    }
  },
  methods: {
    decide (choice) {
      this.$refs.tinder.decide(choice)
    },
    alertClose: function () {
      let alert = document.getElementById("myAlert")
      alert.style.display = "none"
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    toggle: function () {
      let modal = document.getElementById("my-modal")
      modal.style.display = "block"
      this.getMovie()
    },
    endModal: function () {
      let modal = document.getElementById("my-modal")
      modal.style.display = "none"
    },
    getMovie: function () {
      const url = process.env.VUE_APP_URL + `movies/get/random/`
        axios({
          method: 'get',
          url: url,
          headers: this.setToken(),
        })
          .then((res)=>{
            this.movie = res.data
          })
          .catch((err) => {
            console.log(err)
            let modal = document.getElementById("my-modal")
            modal.style.display = "none"
            let alert = document.getElementById("myAlert")
            alert.style.display = "block"
          })
    },
    createComment: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movie.id}/comment/`
        axios({
          method: 'post',
          url: url,
          headers: this.setToken(),
          data: {
            content: '',
            rate: this.rate
          }
        })
          .then(()=>{
            this.getMovie()
            this.rate = 3
          })
          .catch(() => {

          })
    },
    
  },
  created: function () {
    
  }
}
</script>

<style>

</style>