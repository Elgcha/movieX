<template>
  <div class="rounded">
    <div v-if="article" class="mt-3 text-white">
      <div class="flex justify-between p-3 text-left bg-gray-600 border-t border-b border-gray-400 rounded">
        <h3 class="text-xl">{{ article.title }}</h3>
        <div class="my-auto text-sm">{{ article.created_at.slice(0,10) + ' ' + article.created_at.slice(11, 16) }}</div>
      </div>
      <div class="flex justify-between p-3 text-left border-b border-gray-400">
        <span class="flex">
          <img class="object-cover w-5 h-5 my-auto mr-2 border-2 rounded-full" :src="profileImage" alt="profile">
          <span class="my-auto cursor-pointer" @click="moveToProfile(article.username)">{{ article.username }}</span>
        </span>
        <span class="my-auto">조회수: {{ article.views_num }}</span>
      </div>
      <div class="p-3 mb-3 text-left border-b border-gray-400" style="min-height:30vh;">
        <p>{{ article.content }}</p>
      <p v-if="article.created_at !== article.updated_at" class="text-sm text-gray-300">{{ article.updated_at.slice(0,10) + ' ' + article.updated_at.slice(11, 16) }}에 수정됨</p>
      </div>
      <div class="flex justify-end">
        <button class="mx-1 border btn btn-blue btn-blue:hover" @click="back">목록</button>
        <button class="mx-1 bg-yellow-500 border btn btn-blue btn-blue:hover" @click="updateArticle">수정</button>
        <button class="mx-1 bg-red-600 border btn btn-blue btn-blue:hover" @click="deleteArticle">삭제</button>
      </div>
    </div>
    <div>
      <forum-comment :article="article"></forum-comment>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import ForumComment from '@/components/community/ForumComment.vue'
import {mapState} from 'vuex'

export default {
  components: { ForumComment },
  name: 'ArticleDetail',
  data: function () {
    return {
      articlePk: this.$route.params.articlePk,
      article: {},
      username: localStorage.getItem('username'),
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
    viewCount: function () {
      const url = process.env.VUE_APP_URL + `community/${this.articlePk}/views/`
      axios({
        method: 'post',
        url: url,
        headers: this.setToken(),
      })
        .then(() => {
          
        })
        .catch(err => {
          console.log(err)
        })
    },
    getArticle: function () {
      const url = process.env.VUE_APP_URL + `community/${this.articlePk}`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.article = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    updateArticle: function () {
      this.$router.push({name: 'ArticleUpdate', params: {articlePk: this.articlePk}})
    },
    deleteArticle: function () {
      const url = process.env.VUE_APP_URL + `community/${this.articlePk}/`
      axios({
        method: 'delete',
        url: url,
        headers: this.setToken(),
      })
        .then(()=> {
          this.$router.push({name:'Forum'})
        })
        .catch(err => {
          console.log(err)
        })
    },
    back: function () {
      this.$router.push({name:'Forum'})
    },
    moveToProfile: function (username) {
      this.$router.push({name:'Profile', params: {username:username}})
    }
  },
  created: function () {
    this.getArticle()
    this.viewCount()
  },
  computed: {
    ...mapState([
      'isLogin'
    ]),
    profileImage: function () {
      const img = process.env.VUE_APP_URL.slice(0, -1) + this.article.user_image.image_path
      return img
    },
  }
}
</script>

<style>

</style>