<template>
  <div>
    <button @click="ArticleCreate">글 작성</button>
    <table class="text-white bg-gray-700 border border-collapse table-fixed">
      <thead>
        <tr>
          <th class="w-1/2 border">Title</th>
          <th class="w-1/4 border">Author</th>
          <th class="w-1/4 border">Time</th>
          <!-- <th>Views</th> -->
        </tr>
      </thead>
      <tbody>
        <tr v-for="article in articles" :key="article.id" @click="ArticleDetail(article)" class="cursor-pointer hover:bg-gray-600">
          <td class="">{{ article.title }}</td>
          <td class="">{{ article.username }}</td>
          <td>{{ article.created_at }}</td>
          <!-- <td>{{ article }}</td> -->
        </tr>
      </tbody>
    </table>
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
          this.articles = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    ArticleDetail : function (article) {
      this.$router.push({name: 'ArticleDetail', params: {articlePk: article.id}})
    }
  },
  created: function() {
    this.getArticles()
  }
}
</script>

<style>

</style>