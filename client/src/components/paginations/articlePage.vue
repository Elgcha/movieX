<template>
  <div class="flex flex-wrap">
    <div v-for="article in pagenatedArticles" :key="article.id" class='grid w-full grid-cols-2 gap-2 p-2 text-left bg-gray-700 border hover:bg-gray-600 popular' @click="moveToArticleDetail(article.item.id)">
        <div class="text-white">
          <p>{{ article.item.title }}</p>
        </div>
      </div>
      <!-- 페이지네이션 -->
      <div class="container flex justify-center mx-auto my-2">
        <ul class="flex">
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 hover:bg-gray-100" :disabled="pageNum === 0" @click="prevPage">Prev</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 1" @click="pageNum=0">1</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum > 2" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum" @click="prevPage">{{ pageNum }}</button></li>
            <li><button class="h-10 px-5 text-white bg-gray-600 border border-r-0 border-gray-600 ">{{ pageNum + 1 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600 hover:bg-gray-100" v-if="pageNum < pageCount - 1" @click="nextPage">{{ pageNum + 2 }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 3" >...</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" @click="pageNum=pageCount-1">{{ pageCount }}</button></li>
            <li><button class="h-10 px-5 text-gray-600 bg-white border border-gray-600 hover:bg-gray-100" :disabled="pageNum >= pageCount - 1" @click="nextPage">Next</button></li>
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