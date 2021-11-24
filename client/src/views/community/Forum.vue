<template>
  <div>
    
    <!-- 게시판 부분 -->
    
    <table class="w-full text-white rounded table-fixed bg-gradient-to-r from-gray-900 to-gray-800">
      <thead>
        <tr>
          <th class="w-6/12">Title</th>
          <th class="w-4/12">Author</th>
          <th class="w-1/12">Time</th>
          <th class="w-1/12">Views</th>
        </tr>
      </thead>
      
      <tbody class="divide-y divide-gray-500 rounded">
        <tr v-for="article in pagenatedArticles" :key="article.id"  class="rounded cursor-pointer hover:bg-gray-600"  @click="ArticleDetail(article)">
          <td class="p-2 px-4 text-left rounded">{{ article.title }}</td>
          <td class="p-2">{{ article.username }}</td>
          <td class="p-2">{{ calDate(article.created_at) }}</td>
          <td class="p-2 rounded">{{ article.views_num }}</td>
          <hr>
        </tr>
      </tbody>
    </table>
    <div class="flex justify-end mt-1">
      <button class="m-1 btn btn-blue" @click="ArticleCreate">글 작성</button>
    </div>
    <div class="container flex justify-center mx-auto my-2">
        <ul class="flex">
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 rounded-l hover:bg-gray-100" :disabled="pageNum === 0" @click="prevPage">Prev</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 1" @click="pageNum=0">1</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 2" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum" @click="prevPage">{{ pageNum }}</button></li>
            <li><button class="h-10 px-5 text-white bg-gray-600 border border-r-0 border-gray-600 ">{{ pageNum + 1 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 hover:bg-gray-100" v-if="pageNum < pageCount - 1" @click="nextPage">{{ pageNum + 2 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 3" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" @click="pageNum=pageCount-1">{{ pageCount }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-gray-600 rounded-r hover:bg-gray-100" :disabled="pageNum >= pageCount - 1" @click="nextPage">Next</button></li>
        </ul>
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
      pageNum: 0,
    }
  },
  props: {
    pageSize: {
      type: Number,
      required: false,
      default: 20
    },
  },
  computed: {
    pageCount: function() {
      let articleNum = this.articles.length
      let articleSize = this.pageSize
      let page = Math.floor((articleNum-1) / articleSize) + 1
      return page
    },
    pagenatedArticles: function () {
      const start = this.pageNum * this.pageSize
      const end = start + this.pageSize
      return this.articles.slice(start, end)
    }
  },
  methods: {
    calDate: function (date) {
      const Day = new Date()
      if (date.slice(0,10) == Day.getFullYear() + '-' + (Day.getMonth()+1) + '-' + Day.getDate()){
        return date.slice(11,16)
      } else {
        return date.slice(5, 10)
      }
    },
    nextPage: function () {
      this.pageNum += 1;
    },
    prevPage: function () {
      this.pageNum -= 1;
    },
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