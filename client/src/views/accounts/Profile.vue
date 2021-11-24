<template>
  <div class="text-white" >
    <!-- follower modal -->
    <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"  role="alert" id="myAlert3">
      <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg top-20 w-96">
        <div v-if="mydata.followers[0]">
          <div v-for="(follower, index) in mydata.followers" :key="index">{{follower}}</div>
        </div>
        <div v-else>
          아직 팔로워가 없어요....
        </div>
      <span class="absolute inset-y-0 right-0 flex items-center mr-4" @click="alertClose">
        <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
      </span>
      </div>
    </div>
    <!-- following modal -->
    <div class="fixed inset-0 z-10 hidden w-full h-full overflow-y-auto bg-gray-600 bg-opacity-50"  role="alert" id="myAlert4">
      <div class="relative p-5 mx-auto text-white bg-gray-600 border rounded-md shadow-lg top-20 w-96">
        <div v-if="mydata.followings[0]">
          <div v-for="(following, index) in mydata.followings" :key="index">{{following}}</div>
        </div>
        <div v-else>
          아직 아무도 팔로우하지 않았어요...
        </div>
      <span class="absolute inset-y-0 right-0 flex items-center mr-4" @click="alertClose">
        <svg class="w-4 h-4 transform fill-current hover:scale-110" role="button" viewBox="0 0 20 20"><path d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd" fill-rule="evenodd"></path></svg>
      </span>
      </div>
    </div>

    <main class="mt-3 bg-gray-100 bg-opacity-25" style="min-height:100vh;">
      <div class="mb-8 lg:mx-auto">
        <header class="flex flex-wrap items-center w-8/12 p-4 md:py-8">
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



              <!-- follow button -->
              <div v-if="!sameperson" @click="follow" class="block px-2 py-1 text-sm font-semibold text-center text-white bg-blue-500 rounded cursor-pointer sm:inline-block">Follow</div>
            </div>

            <!-- post, following, followers list for medium screens -->
            <ul class="hidden mb-4 space-x-8 md:flex">
              <li>
                <span class="font-semibold">{{ me.article_set.length }}</span>
                articles
              </li>

              <li>
                <span class="font-semibold cursor-pointer" @click="openFollowers">{{ me.followers.length }}</span>
                followers
              </li>
              <li>
                <span class="font-semibold cursor-pointer" @click="openFollowings">{{ me.followings.length }}</span>
                following
              </li>
            </ul>

            <!-- user meta form medium screens -->
            

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
          <div class="h-full"  style="min-heigth:20vh;">
            <!-- column -->
            <div v-swiper:mySwiperT="swiperOption" class="h-full my-2 swiper-container">
              <div class="h-full bg-dark swiper-wrapper">
                <div
                v-for="movie in wantMovies"
                :key="movie.id"
                :movie="movie"
                class="justify-center h-auto swiper-slide"
                >
                  <div class='w-full h-auto cursor-pointer popular' @click="moveToDetail(movie.id)">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + movie.poster_path" alt="" class="object-cover w-full h-full transform hover:scale-110">
                  </div>
                </div>
                </div>

              <div class="swiper-button-prev" slot="button-prev"></div> 
              <div class="swiper-button-next" slot="button-next"></div>


            </div>

          </div>
          <h2> 평가한 영화</h2>
          <div class="h-full">
            <!-- column -->
            <div v-swiper:mySwiperR="swiperOptionR" class="h-full swiper-container">
              <div class="h-full p-2 bg-dark swiper-wrapper">
                <div
                v-for="movie in evalMovies"
                :key="movie.id"
                :movie="movie"
                class="justify-center h-auto swiper-slide"
                >
                  <div class='w-full h-auto cursor-pointer popular' @click="moveToDetail(movie.id)">
                    <img :src="'https://image.tmdb.org/t/p/w500/' + movie.movie.poster_path" alt="" class="object-cover w-full h-full transform hover:scale-110">
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
      mydata: null,
      isFollowed: false,
      wantMovies: [],
      evalMovies: [],
      swiperOption: {
        slidesPerView: 6,
        spaceBetween: 10,
        loop: false,
        breakpoints: {
          320: {
            slidesPerView: 2,
            spaceBetween: 10
          },
          480: {
            slidesPerView: 3,
            spaceBetween: 15
          },
          640: {
            slidesPerView: 4,
            spaceBetween: 20
          },
          1280: {
            slidesPerView: 6,
            spaceBetween: 20
          }
        },
        navigation: {
          nextEl: '.swiper-button-next', 
          prevEl: '.swiper-button-prev' 
        },
      },
      swiperOptionR: {
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
            spaceBetween: 10
          },
          480: {
            slidesPerView: 3,
            spaceBetween: 15
          },
          640: {
            slidesPerView: 4,
            spaceBetween: 20
          },
          1280: {
            slidesPerView: 6,
            spaceBetween: 20
          }
        },
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
    openFollowers: function () {
      let alert = document.getElementById("myAlert3")
      alert.style.display = "block"
    },
    openFollowings: function () {
      let alert = document.getElementById("myAlert4")
      alert.style.display = "block"
    },
    alertClose: function () {
      let alert = document.getElementById("myAlert3")
      let alert1 = document.getElementById("myAlert4")
      alert.style.display = "none"
      alert1.style.display = "none"
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    getEvalMovies: function () {
      const username = this.$route.params.username
      const url = process.env.VUE_APP_URL + `accounts/profile/${username}/recommend/` // profile/<username>/recommend/
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          console.log(res)
          this.evalMovies = res.data.moviecomment_set_name
        })
        .catch(err => {
          console.log(err)
        })
    },
    getmyData: function () {
      const username = this.$route.params.username
      const url = process.env.VUE_APP_URL + `accounts/profile/${username}/follow/list/` // profile/<username>/follow/list/
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          console.log(res)
          this.mydata = res.data
        })
        .catch(err => {
          console.log(err)
        })
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
    this.getEvalMovies()
    this.getmyData()
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