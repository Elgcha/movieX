<template>
  <div class="w-full text-white" style="min-height:50vh;">
    <div class="w-full">
      <label class="block m-2 text-lg font-bold text-left text-white" for="title">제목 </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:border-green-800" type="text" @input="inputTitle" id='title'>
    </div>
    <div class="w-full">
      <label class="block m-2 text-lg font-bold text-left text-white" for="content">내용 </label>
      <textarea class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:border-green-800" @input="inputContent" id='content' style="min-height:20vh"></textarea>
    </div>
    <button @click="ArticleCreate" class="m-3 btn btn-blue">작성</button>
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