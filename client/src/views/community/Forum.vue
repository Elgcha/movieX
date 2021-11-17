<template>
  <div>
    <button @click="ArticleCreate">글 작성</button>
    <div v-for="article in articles" :key="article.id">
      <p>제목 : {{ article.title }}</p>
      
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Forum',
  data: function () {
    return {
      articles: [],
    }
  },
  methods: {
    ArticleCreate: function () {
      this.$router.push({name: 'ArticleCreate'})
    },
    ArticleDetail: function (event) {
      console.log(event.target)
      // this.$router.push({name: 'ArticleDetail', params: {articlePk: event.target.}})
    },
    getArticles: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/community/'
      })
        .then(res => {
          console.log(res)
          this.articles = res.data
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  created: function() {
    this.getArticles()
  }
}
</script>

<style>

</style>