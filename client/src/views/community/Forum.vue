<template>
  <div>
    <button @click="ArticleCreate">글 작성</button>
    
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
    getArticles: function () {
      axios({
        method: 'get',
        url: 'http://127.0.0.1:8000/community/'
      })
        .then(res => {
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>

<style>

</style>