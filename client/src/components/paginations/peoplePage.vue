<template>
  <div class="flex flex-wrap">
    <div v-for="people in pagenatedPeoples" :key="people.id" class='grid grid-cols-2 gap-2 p-2 rounded cursor-pointer hover:border-gray-600 hover:bg-gray-800 flex-3 popular' @click="moveToPeopleDetail(people.item.id)">
        <img :src="'https://image.tmdb.org/t/p/w500/' + people.item.profile_path" alt="profile" class="object-cover h-full p-3 transform cursor-pointer hover:scale-105">
        <div class="mt-6 text-lg text-white">
          <p>{{ people.item.name }}</p>
        </div>
      </div>
      <!-- 페이지네이션 -->
      <div class="relative w-full mx-auto mb-20">
        
      <div class="container absolute w-full mx-auto my-2" style="left:34vw">
        <ul class="flex w-full mx-auto">
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 rounded-l hover:bg-gray-500" :disabled="pageNum === 0" @click="prevPage">Prev</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum > 1" @click="pageNum=0">1</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600" v-if="pageNum > 1" >...</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum" @click="prevPage">{{ pageNum }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500">{{ pageNum + 1 }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum < pageCount - 1" @click="nextPage">{{ pageNum + 2 }}</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600" v-if="pageNum < pageCount - 2" >...</button></li>
            <li><button class="h-10 px-5 text-white border border-r-0 border-gray-600 hover:bg-gray-500" v-if="pageNum < pageCount - 2" @click="pageNum=pageCount-1">{{ pageCount }}</button></li>
            <li><button class="h-10 px-5 text-white border border-gray-600 rounded-r hover:bg-gray-500" :disabled="pageNum >= pageCount - 1" @click="nextPage">Next</button></li>
        </ul>
    </div>
      </div>
  </div>
</template>

<script>
export default {
  name: 'peoplePage',
  data: function () {
    return {
      pageNum: 0
    }
  },
  props: {
    peoples: {
      type: Array,
    },
    pageSize: {
      type: Number,
      required: false,
      default: 12
    },
  },
  methods: {
    nextPage: function () {
      this.pageNum += 1;
    },
    prevPage: function () {
      this.pageNum -= 1;
    },
    moveToPeopleDetail: function (peoplePk) {
      this.$router.push({name: 'PeopleDetail', params: {peoplePk: peoplePk}})
    },
  },
  computed: {
    pageCount: function() {
      let peopleNum = this.peoples.length
      let peopleSize = this.pageSize
      let page = Math.floor((peopleNum-1) / peopleSize) + 1
      return page
    },
    pagenatedPeoples: function () {
      const start = this.pageNum * this.pageSize
      const end = start + this.pageSize
      return this.peoples.slice(start, end)
    }
  },
}
</script>

<style>

</style>