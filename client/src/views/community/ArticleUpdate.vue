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
    <button @click="ArticleUpdate">제출</button>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'ArticleUpdate',
  data: function () {
    return {
      articlePk: this.$route.params.articlePk,
      Article: {
        title: null,
        content: null,
      }
    }
  },
  methods: {
    // 정보 입력
    inputTitle: function(event) {
      this.Article.title = event.target.value
    },
    inputContent: function(event) {
      this.Article.content = event.target.value
    },
    // 원래 정보 입력
    getArticle: function () {
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/community/${this.articlePk}/`
      })
        .then(res => {
          console.log(res)
          this.Article.title = res.data.title
          this.Article.content = res.data.content
          const title = document.querySelector('#title')
          const content = document.querySelector('#content')
          title.value = res.data.title
          content.value = res.data.content
        })
        .catch(err => {
          console.log(err)
        })
    },
    // 게시글 수정
    ArticleUpdate: function() {
      axios({
        method: 'put',
        url: `http://127.0.0.1:8000/community/${this.articlePk}/`,
        data: this.Article,
      })
        .then(()=>{
          
        })
        .catch(() => {

        })
    },
    
  },
  created: function () {
    this.getArticle()
  }
}
</script>

<style>

</style>