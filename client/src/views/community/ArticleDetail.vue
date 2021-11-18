<template>
  <div>
    <div v-if="article" class="text-white">
      <h3>제목: {{ article.title }}</h3>
      <p>내용 : {{ article.content }}</p>
      <p>작성일 : {{ article.created_at }}</p>
      <p>수정일 : {{ article.updated_at }}</p>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="updateArticle">수정</button>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="deleteArticle">삭제</button>
      <button class="mx-1 border btn btn-blue btn-blue:hover" @click="back">>back</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ArticleDetail',
  data: function () {
    return {
      articlePk: this.$route.params.articlePk,
      article: {},
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
  }
}
</script>

<style>

</style>