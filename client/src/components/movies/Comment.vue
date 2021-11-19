<template>
  <div>
  <div v-if="isLogin" class="w-1/2 p-2 pt-4 rounded ">
    <div class="w-full p-3 mt-3">
      <textarea rows="3" class="w-full p-2 border rounded" @input="inputChange" placeholder="" id="Moviecontent"></textarea>
    </div>
    <div class="flex justify-between mx-3">
        <div class="mx-auto space-x-4 star-rating">
          <input type="radio" id="5-stars" name="rating" value="10" v-model="ratings"/>
          <label for="5-stars" class="pr-4 star">★</label>
          <input type="radio" id="4-stars" name="rating" value="8" v-model="ratings"/>
          <label for="4-stars" class="star">★</label>
          <input type="radio" id="3-stars" name="rating" value="6" v-model="ratings"/>
          <label for="3-stars" class="star">★</label>
          <input type="radio" id="2-stars" name="rating" value="4" v-model="ratings"/>
          <label for="2-stars" class="star">★</label>
          <input type="radio" id="1-star" name="rating" value="2" v-model="ratings" />
          <label for="1-star" class="star">★</label>
        </div>
      <div><button 
      @click="createComment"
      class="px-4 py-1 font-light text-white bg-gray-800 rounded hover:bg-gray-700"
      >
      Submit
      </button></div>
      <div>
      </div>
    </div>
  </div>
  <div v-if="comments">
    <h3>댓글 목록</h3>
    <div v-for="comment in comments" :key="comment.id">
      {{comment.content}}
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'
import {mapState} from 'vuex'

export default {
  name: 'Comment',
  data: function () {
    return {
      content: null,
      comments: null,
      ratings: null,
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
          console.log(res)
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
    this.getComments()
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