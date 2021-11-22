<template>
  <div>
    <div v-if="article" class="mt-3 text-white">
      <div class="flex justify-between p-3 text-left bg-gray-600 border-t border-b">
        <h3 class="text-xl">{{ article.title }}</h3>
        <div class="my-auto text-sm">{{ article.created_at.slice(0,10) + ' ' + article.created_at.slice(11, 16) }}</div>
      </div>
      <div class="p-3 text-left border-b">{{ article.username }}</div>
      <div class="p-3 mb-3 text-left border-b" style="min-height:30vh;">
        <p>{{ article.content }}</p>
      </div>
      <p v-if="article.created_at !== article.updated_at">{{ article.updated_at.slice(0,10) + ' ' + article.updated_at.slice(11, 16) }}에 수정됨</p>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="back">목록</button>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="updateArticle">수정</button>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="deleteArticle">삭제</button>
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
    getArticle: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/community/${this.articlePk}/`
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
      axios({
        method: 'delete',
        url: `http://127.0.0.1:8000/community/${this.articlePk}/`
      })
        .then(()=> {

        })
        .catch(err => {
          console.log(err)
        })
    },
    back: function () {
      this.$router.push({name:'Forum'})
    },
  },
  created: function () {
    this.getArticle()
  },
  computed: {
    ...mapState([
      'isLogin'
    ]),
  }
}
</script>

<style>

</style>