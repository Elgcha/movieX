<template>
  <div>
  <div v-if="isLogin" class="w-1/2 p-2 pt-4 rounded ">
    <p class="text-left">평가 작성</p>
    <div class="flex justify-between mx-3 mt-3" >
        <star-rating v-model="ratings"></star-rating>
      <div>
      </div>
    </div>
    <div class="flex w-full p-3">
      <input v-if="comment_user.indexOf(username) < 0" type="text" rows="3" class="w-full p-2 text-black bg-white border rounded" @input="inputChange" placeholder="" id="Moviecontent">
      <input v-else v-show="wantEdit" type="text" rows="3" class="w-full p-2 text-black bg-white border rounded" @input="inputChange" placeholder="" id="Moviecontent">
      <button 
      @click="editClick"
      class="h-full px-4 py-2 font-light text-white bg-gray-400 rounded hover:bg-gray-600"
      v-if="comment_user.indexOf(username) >= 0"
      v-show="!wantEdit"
      >
      Edit
      </button>
      <div><button 
      @click="createComment"
      class="h-full px-4 py-2 font-light text-white bg-gray-400 rounded hover:bg-gray-600"
      v-if="comment_user.indexOf(username) < 0"
      >
      Submit
      </button>
      <button 
      @click="editComment"
      class="h-full px-4 py-2 font-light text-white bg-gray-400 rounded hover:bg-gray-600"
      v-else
      v-show="wantEdit"
      >
      Edit
      </button></div>
    </div>
  </div>
  <div v-else class="text-left">댓글 작성을 위해선 <span class="text-blue-500 cursor-pointer" @click="moveToLogin">로그인</span>이 필요합니다.</div>
  <h3 class="mt-3 mb-5 text-xl text-left">댓글 목록</h3>
  <div v-if="comments" class="">
    <div v-for="(comment, index) in comments" :key="index" class="px-3 py-1 text-left">
      <div>
        <div class="flex w-full px-2 bg-gray-700 rounded">

          <img class="object-cover w-5 h-5 my-auto mr-2 border-2 rounded-full" :src="profileImage + comment.user_image.image_path" alt="profile">
          <p @click="moveToProfile(comment.username)" class="p-2 my-auto cursor-pointer">{{comment.username}}</p>

          <div class="flex ml-3 mr-auto">
            <div v-for="i in 5" :class="{ 'mr-1': i < 5 }" :key="i" class="my-auto text-sm d-inline">
              <svg class="block w-6 h-6" :class="[ comment.rate >= i ? 'text-yellow-500': 'text-grey-500']" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
            </div>
          </div>
          <v-btn v-if="comment.username === username" class="p-3 m-2 my-auto cursor-pointer" @click="deleteComment">delete</v-btn>
        </div>
        <p class="p-2">{{comment.content}}</p>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import {mapState} from 'vuex'
import starRating from '../ratings/starRating.vue'

export default {
  components: { starRating },
  name: 'Comment',
  data: function () {
    return {
      content: null,
      comments: null,
      ratings: null,
      comment_user: [],
      username: localStorage.getItem('username'),
      wantEdit: false,
    }
  },
  computed: {
    ...mapState([
      'isLogin'
    ]),
    movieId: function () {
      return this.movie.id
    },
    profileImage: function () {
      const img = process.env.VUE_APP_URL.slice(0, -1)
      return img
    },
  },
  methods: {
    getProfile: function () {
      const url = process.env.VUE_APP_URL + `accounts/profile/get/self/`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.username = res.data.username
        })
        .catch(err => {
          console.log(err)
        })
    },
    editClick: function () {
      this.wantEdit = true
      this.comments.map(comment => {
        if (comment.username === this.username) {
          this.ratings = comment.rate
          const contentInput = document.querySelector('#Moviecontent')
          contentInput.value = comment.content
          this.content =comment.content
        }
      })
    },
    moveToProfile: function (username) {
      this.$router.push({name:'Profile', params: {username:username}})
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    inputChange: function(event) {
      this.content = event.target.value
    },
    getComments: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/comment/list/`
      const key = this.setToken()
      axios({
        method: 'get',
        url: url,
        headers: key,
      })
        .then(res => {
          this.comments = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    createComment: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/comment/`
      const key = this.setToken()

      axios({
        method: 'post',
        url: url,
        headers: key,
        data: {
          content: this.content,
          rate: this.ratings ,
        },
      })
        .then(() => {
          this.content = null
          const contentInput = document.querySelector('#Moviecontent')
          contentInput.value = null
          this.getComments()
        })
        .catch(err => {
          console.log(err)
        })
      
    },
    editComment: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/${this.username}/`
      const key = this.setToken()

      axios({
        method: 'put',
        url: url,
        headers: key,
        data: {
          content: this.content,
          rate: this.ratings,
        },
      })
        .then(() => {
          this.content = null
          const contentInput = document.querySelector('#Moviecontent')
          contentInput.value = null
          this.wantEdit=false
          this.getComments()
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteComment: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/${this.username}/`
      const key = this.setToken()

      axios({
        method: 'delete',
        url: url,
        headers: key,
      })
        .then(() => {
          this.content = null
          const contentInput = document.querySelector('#Moviecontent')
          contentInput.value = null
          this.wantEdit=false
          this.getComments()
        })
        .catch(err => {
          console.log(err)
        })
    },
    moveToLogin: function () {
      this.$router.push({name:'Login'})
    }
  },
  props: {
    movie: {
      type: Object,
    }
  },
  created: function () {
    this.getComments()
    this.getProfile()
  },
  watch: {
    // 평가 정보 가져오기
    movie: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/comment/list/`
      const key = this.setToken()
      axios({
        method: 'get',
        url: url,
        headers: key,
      })
        .then(res => {
          this.comments = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    comments: function() {
      const username = []
      this.comments.map(comment => {
        username.push(comment.username)
      })
      this.comment_user = username
    }
  },
  updated: function () {
    this.$emit('changeOccur')
  },
}
</script>

<style>
.star-rating {
  display: flex;
  flex-direction: row-reverse;
  font-size: 2.25rem;
  line-height: 2.5rem;
  justify-content: space-around;
  padding: 0 0.2em;
  text-align: center;
  width: 5em;
}
 
.star-rating input {
  display: none;
}
 
.star-rating label {
  -webkit-text-fill-color: transparent; /* Will override color (regardless of order) */
  -webkit-text-stroke-width: 2.3px;
  -webkit-text-stroke-color: #2b2a29;
  cursor: pointer;
}
 
.star-rating :checked ~ label {
  -webkit-text-fill-color: gold;
}
 
.star-rating label:hover,
.star-rating label:hover ~ label {
  -webkit-text-fill-color: #fff58c;
}
</style>