<template>
<div>
  <div v-if="isLogin" class="w-1/2 p-2 pt-4 rounded ">
    <div class="w-full p-3 mt-3">
      <textarea rows="3" class="w-full p-2 border rounded" @input="inputChange" placeholder="" id="content"></textarea>
    </div>
    <div class="flex justify-between mx-3">
      <div><button 
      @click="createComment"
      class="px-4 py-1 font-light text-white bg-gray-800 rounded hover:bg-gray-700"
      >
      Submit
      </button></div>
      
    </div>
  </div>
  <div>
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
  name: 'ForumComment',
  data: function () {
    return {
      content: null,
      comments: [],
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
    getComments: function () {
      const url = process.env.VUE_APP_URL + `community/${this.articleId}/comment/create/`
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
      const url = process.env.VUE_APP_URL + `community/${this.articleId}/comment/create/`
      const key = this.setToken()

      axios({
        method: 'post',
        url: url,
        headers: key,
        data: {
          content: this.content,
        }
      })
        .then(() => {
          this.content = null
          const contentInput = document.querySelector('#content')
          contentInput.value = null
          this.getComments()
        })
        .catch(err => {
          console.log(err)
        })
      
    },
    inputChange: function(event) {
      this.content = event.target.value
    }
  },
  props: {
    article: {
      type: Object,
    }
  },
  computed: {
    ...mapState([
      'isLogin'
    ]),
    articleId: function () {
      return this.article.id
    }
  },
  watch: {
    article: function () {
      this.getComments()
    }
  }
}
</script>

<style>

</style>