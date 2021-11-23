<template>
<div class="text-white">
  <div v-if="isLogin" class="w-1/2 p-2 pt-4 rounded ">
    <div class="w-full p-3 mt-3">
      <textarea rows="3" class="w-full p-2 text-black border rounded" @input="inputChange" placeholder="" id="content"></textarea>
    </div>
    <div class="flex justify-between mx-3">
      <div><button 
      @click="createComment"
      class="px-4 py-1 font-light text-white bg-gray-500 rounded hover:bg-gray-700"
      >
      Submit
      </button></div>
      
    </div>
  </div>
  <div v-else class="text-left">댓글 작성을 위해선 <span class="text-blue-500 cursor-pointer" @click="moveToLogin">로그인</span>이 필요합니다.</div>
  <h3 class="text-xl text-left">댓글 목록</h3>
  <div v-if="comments" class="p-2 text-left">
    <div v-for="comment in comments" :key="comment.id" class="p-1 m-1 ">
      <div class="p-2 bg-gray-700 rounded" ><span @click="moveToProfile(comment.username)" class="cursor-pointer">{{comment.username}}</span></div>
      <div class="p-2">{{comment.content}}</div>
      <input v-show="edited===comment.id" type="text" class="w-full p-2 text-black bg-gray-200 border rounded" id="editInput" @input="editInputChange">
      <div v-if="comment.username === username" class="flex justify-end">
        <div v-if="!edited" class="m-2 mb-0 btn btn-blue" @click="editStart(comment.id, comment.content)">수정</div>
        <div v-if="edited===comment.id" class="m-2 mb-0 btn btn-blue" @click="updateComment(comment.id)">완료</div>
        <div class="m-2 mb-0 btn btn-blue" @click="deleteComment(comment.id)">삭제</div>
      </div>
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
      edited: null,
      editContent: null,
      content: null,
      comments: [],
      username: localStorage.getItem('username')
    }
  },
  methods: {
    editStart: function (commentId, commentContent) {
      this.edited = commentId
      this.editContent = commentContent
      const input = document.querySelector('#editInput')
      input.value = commentContent
    },
    editInputChange: function (event) {
      this.editContent = event.target.value
    },
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
    moveToProfile: function (username) {
      this.$router.push({name:'Profile', params: {username:username}})
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
    updateComment: function (comment_pk) {
      const url = process.env.VUE_APP_URL + `community/${this.articleId}/comment/${comment_pk}/update/`
      const key = this.setToken()

      axios({
        method: 'put',
        url: url,
        headers: key,
        data: {
          content: this.editContent,
        }
      })
        .then(() => {
          this.content = null
          const contentInput = document.querySelector('#content')
          contentInput.value = null
          this.edited = null
          this.getComments()
        })
        .catch(err => {
          console.log(err)
        })
    },
    deleteComment: function (comment_pk) {
      const url = process.env.VUE_APP_URL + `community/${this.articleId}/comment/${comment_pk}/update/`
      const key = this.setToken()

      axios({
        method: 'delete',
        url: url,
        headers: key,
      })
        .then(() => {
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
  },
  created: function () {
    this.getComments()
  }
}
</script>

<style>

</style>