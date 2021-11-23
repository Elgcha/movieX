<template>
  <div>
    <h1>글 작성</h1>
    <div class="w-full">
      <label class="block m-2 text-lg font-bold text-left text-white" for="title">제목 </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:border-green-800" type="text" @input="inputTitle" id='title'>
    </div>
    <div class="w-full">
      <label class="block m-2 text-lg font-bold text-left text-white" for="content">내용 </label>
      <textarea class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:border-green-800" @input="inputContent" id='content' style="min-height:20vh"></textarea>
    </div>
    <button @click="ArticleUpdate" class="m-3 btn btn-blue">수정</button>
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
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
    // 정보 입력
    inputTitle: function(event) {
      this.Article.title = event.target.value
    },
    inputContent: function(event) {
      this.Article.content = event.target.value
    },
    // 원래 정보 입력
    getArticle: function () {
      const url = process.env.VUE_APP_URL + `community/${this.articlePk}`
      axios({
        method: 'get',
        url: url,
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
      const url = process.env.VUE_APP_URL + `community/${this.articlePk}`
      axios({
        method: 'put',
        url: url,
        data: this.Article,
        headers: this.setToken(),
      })
        .then(()=>{
          this.$router.push({name:'ArticleDetail', params:{articlePk:this.articlePk}})
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