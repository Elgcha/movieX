<template>
  <div>
    <h1>글 작성</h1>
    <div>
      <label for="title">제목 </label>
      <input type="text" @input="inputTitle" id='title'>
    </div>
    <div>
      <label for="content">내용 </label>
      <input type="text" @input="inputContent" id='content'>
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