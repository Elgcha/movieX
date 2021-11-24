<template>
  <div class="flex flex-wrap">
    <table class="w-full text-white rounded table-fixed bg-gradient-to-r from-gray-900 to-gray-800">
      <thead>
        <tr class="">
          <th class="w-6/12 p-1">Title</th>
          <th class="w-4/12 p-1">Author</th>
          <th class="w-1/12 p-1">Time</th>
          <th class="w-1/12 p-1">Views</th>
        </tr>
      </thead>
      
      <tbody class="divide-y divide-gray-500">
        <tr v-for="article in pagenatedArticles" :key="article.id"  class="cursor-pointer hover:bg-gray-600"  @click="moveToArticleDetail(article.item.id)">
          <td class="p-2 px-4 text-left rounded-l">{{ article.item.title }}</td>
          <td class="p-2">{{ article.item.username }}</td>
          <td class="p-2">{{ calDate(article.item.created_at) }}</td>
          <td class="p-2 rounded-r">{{ article.item.views_num }}</td>
          <hr>
        </tr>
      </tbody>
    </table>
    <!-- <div v-for="article in pagenatedArticles" :key="article.id" class='grid w-full grid-cols-2 gap-2 p-2 text-left bg-gray-700 border hover:bg-gray-600 popular' @click="moveToArticleDetail(article.item.id)">
        <div class="text-white">
          <p>{{ article.item.title }}</p>
        </div>
      </div> -->
      <!-- 페이지네이션 -->
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
export default {
  name: 'articlePage',
  data: function () {
    return {
      pageNum: 0
    }
  },
  props: {
    articles: {
      type: Array,
    },
    pageSize: {
      type: Number,
      required: false,
      default: 10
    },
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
    moveToArticleDetail: function (articlePk) {
      this.$router.push({name: 'ArticleDetail', params: {articlePk: articlePk}})
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
}
</script>

<style>

</style>