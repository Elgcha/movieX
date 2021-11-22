<template>
  <div class="w-full text-white">
    <h1>글 작성</h1>
    <div class="w-full">
      <label class="block mb-2 text-sm font-bold text-white" for="title">제목 </label>
      <input class="w-4/5 px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" @input="inputTitle" id='title'>
    </div>
    <div class="w-full">
      <label class="block mb-2 text-sm font-bold text-white" for="content">내용 </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" @input="inputContent" id='content'>
    </div>
    <button @click="ArticleCreate">제출</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ArticleCreate',
  data: function () {
    return {
      Article: {
        title: null,
        content: null,
      }
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
    inputTitle: function(event) {
      this.Article.title = event.target.value
    },
    inputContent: function(event) {
      this.Article.content = event.target.value
    },
    ArticleCreate: function() {
      axios({
        method: 'post',
        url: 'http://127.0.0.1:8000/community/create/',
        data: this.Article,
        headers: this.setToken(),
      })
        .then((res)=>{
          this.$router.push({name: 'ArticleDetail', params: {articlePk: res.data.id}})
        })
        .catch(() => {

        })
    }
    
  },
}
</script>

<style>

</style>