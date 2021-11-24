<template>
  <div class="text-white" >
    <main class="mt-3 bg-gray-100 bg-opacity-25" style="min-height:80vh;">
      <div class="mb-8 lg:w-8/12 lg:mx-auto">
        <header class="flex flex-wrap items-center p-4 md:py-8">
          <div class="md:w-3/12 md:ml-16">
            <!-- profile image -->
            <img class="object-cover w-20 h-20 p-1 border-2 border-pink-600 rounded-full md:w-40 md:h-40" :src="profileImage" alt="profile">
          </div>



          <!-- profile meta -->
          <div class="w-8/12 ml-4 md:w-7/12">
            <div class="mb-4 md:flex md:flex-wrap md:items-center">
              <h2 class="inline-block mb-2 text-3xl font-light md:mr-2 sm:mb-0">
                {{ me.username }}
              </h2>

              <!-- badge -->
              <span class="relative inline-block mr-6 text-xl text-blue-500 transform -translate-y-2 fas fa-certificate fa-lg" aria-hidden="true">
                <i class="absolute inset-x-0 mt-px ml-1 text-xs text-white fas fa-check"></i>
              </span>

              <!-- follow button -->
              <div v-if="!sameperson" @click="follow" class="block px-2 py-1 text-sm font-semibold text-center text-white bg-blue-500 rounded sm:inline-block">Follow</div>
            </div>

            <!-- post, following, followers list for medium screens -->
            <ul class="hidden mb-4 space-x-8 md:flex">
              <li>
                <span class="font-semibold">{{ me.article_set.length }}</span>
                articles
              </li>

              <li>
                <span class="font-semibold">{{ me.followers.length }}</span>
                followers
              </li>
              <li>
                <span class="font-semibold">{{ me.followings.length }}</span>
                following
              </li>
            </ul>

            <!-- user meta form medium screens -->
            

          </div>

          <!-- user meta form small screens -->
          <div class="my-2 text-sm md:hidden">
            <h1 class="font-semibold">Mr Travlerrr...</h1>
            <span>Travel, Nature and Music</span>
            <p>Lorem ipsum dolor sit amet consectetur</p>
          </div>

        </header>

        <!-- posts -->
        <div class="px-px md:px-3">

          <!-- user following for mobile only -->
          <ul class="flex justify-around p-2 space-x-8 text-sm leading-snug text-center text-gray-600 border-t md:hidden">
           <li>
              <span class="font-semibold">{{ me.article_set.length }}</span>
              articles
            </li>

            <li>
              <span class="font-semibold">{{ me.followers.length }}</span>
              followers
            </li>
            <li>
              <span class="font-semibold">{{ me.followings.length }}</span>
              following
            </li>
          </ul>

          <!-- insta freatures -->
          <ul class="flex items-center justify-around space-x-12 text-xs font-semibold tracking-widest text-white border-t md:justify-center">
            <!-- posts tab is active -->

            <li>
              <a class="inline-block p-3" href="#">
                <i class="text-xl far fa-square md:text-xs"></i>
                <span class="hidden md:inline">want movies</span>
              </a>
            </li>
            
          </ul>
          <!-- flexbox grid -->
          <div class="-mx-px md:-mx-3">
            <!-- column -->
            <div v-swiper:mySwiper="swiperOption" class="my-2 swiper-container">
              <div class="bg-dark swiper-wrapper">
                <div
                v-for="movie in wantMovies"
                :key="movie.id"
                :movie="movie"
                class="justify-center h-auto swiper-slide"
                >
                  <div class='w-full h-auto cursor-pointer popular' @click="moveToDetail(movie.id)">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="" class="object-cover w-full h-full">
                    <div class="overlay" @click="moveToDetail(movie.id)">
                    <h3 class="description" @click="moveToDetail(movie.id)">{{ movie.title }}</h3>
                  </div>
                </div>
                </div>
              </div>
              <div class="swiper-button-prev" slot="button-prev"></div> 
              <div class="swiper-button-next" slot="button-next"></div>


            </div>

          </div>
        </div>
      </div>
    </main>
    

  </div>
</template>

<script>
import axios from 'axios'
import {mapActions} from 'vuex'

export default {
  name: 'Profile',
  data: function () {
    return {
      file: null,
      me: {},
      isFollowed: false,
      wantMovies: [],
      swiperOption: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        navigation: {
          nextEl: '.swiper-button-next', 
          prevEl: '.swiper-button-prev' 
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
    getProfile: function () {
      const username = this.$route.params.username
      const url = process.env.VUE_APP_URL + `accounts/profile/${username}/`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.me = res.data
          this.wantMovies = res.data.user_wants
        })
        .catch(err => {
          console.log(err)
        })
    },
    follow: function () {
      const username = this.$route.params.username
      const url = process.env.VUE_APP_URL + `accounts/${username}/follow/`
      axios({
        method: 'post',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.isFollowed = res.data.isFollowed
        })
    },
    imageUpload: function (event) {
      const username = this.$route.params.username
      const token = localStorage.getItem('jwt')
      this.file = event.target.files[0]
      if (this.file) {
        let data = new FormData()
        data.append('image', this.file)
        const url = process.env.VUE_APP_URL + `accounts/profiles/${username}/`
        axios({
          method: 'put',
          url: url,
          data: data,
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `JWT ${token}`
          },
        })
          .then(() => {
            this.getProfile()
          })
          .catch(err => {
            console.log(err)
          })
      }
    }
    
  },
  computed: {
    sameperson: function () {
      const username = this.$route.params.username
      const me = localStorage.getItem('username')
      return username === me? true : false
    },
    profileImage: function () {
      const img = process.env.VUE_APP_URL.slice(0, -1) + this.me.image_path
      return img
    }
  },
  created: function () {
    this.getProfile()
  }
}
</script>

<style>
.pb-full {
  padding-bottom: 100%;
}

/* hide search icon on search focus */
.search-bar:focus + .fa-search{
  display: none;
}

@media screen and (min-width: 768px) {
  .post:hover .overlay {
    display: block;
  }
}

</style>