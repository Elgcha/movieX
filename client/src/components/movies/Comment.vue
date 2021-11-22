<template>
  <div>
  <div v-if="isLogin" class="w-1/2 p-2 pt-4 rounded ">
    <p class="text-left">댓글 작성</p>
    <div class="flex w-full p-3 mt-3">
      <input type="text" rows="3" class="w-full p-2 text-black border rounded" @input="inputChange" placeholder="" id="Moviecontent">
      <div><button 
      @click="createComment"
      class="h-full px-4 py-2 font-light text-white bg-gray-400 rounded hover:bg-gray-200"
      >
      Submit
      </button></div>
    </div>
    <div class="flex justify-between mx-3" >
        <star-rating v-model="ratings"></star-rating>
      <div>
      </div>
    </div>
  </div>
  <h3 class="mb-5 text-left">댓글 목록</h3>
  <div v-if="comments" class="divide-y">
    <div v-for="comment in comments" :key="comment.id" class="px-3 py-1 text-left">
      <div>
        <div class="flex">
          <p>{{comment.username}}</p>

          <div v-for="i in 5" :class="{ 'mr-1': i < 5 }" :key="i" class="d-inline">
            <svg class="block w-8 h-8" :class="[ comment.rate / 2 >= i - 1 ? 'text-yellow-500': 'text-grey-500']" fill="currentColor" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 15l-5.878 3.09 1.123-6.545L.489 6.91l6.572-.955L10 0l2.939 5.955 6.572.955-4.756 4.635 1.123 6.545z"/></svg>
          </div>
        </div>
        <p>{{comment.content}}</p>
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
      ratings: 3,
    }
  },
  computed: {
    ...mapState([
      'isLogin'
    ]),
    movieId: function () {
      return this.movie.id
    }
  },
  methods: {
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
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/commentlist/`
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
          rate: this.ratings,
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
  },
  props: {
    movie: {
      type: Object,
    }
  },
  created: function () {
  },
  watch: {
    movie: function () {
      const url = process.env.VUE_APP_URL + `movies/${this.movieId}/commentlist/`
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
    }
  }
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