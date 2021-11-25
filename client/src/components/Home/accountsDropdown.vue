<template>
  <div class="relative p-1 my-auto text-left">
  <div @click="toggleMenu" class="flex">
    <img class="hidden object-cover w-5 h-5 p-1 rounded-full md:w-8 md:h-8 md:block" :src="profileImage" alt="">
    <button type="button" class="inline-flex justify-center w-full p-1 text-sm font-medium text-white rounded-md shadow-sm mydropdown hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-offset-gray-100 focus:ring-indigo-500" id="menu-button" aria-expanded="true" aria-haspopup="true">
      {{ username }}
      <!-- 아래 화살표 이미지 -->
      <svg class="w-5 h-5 ml-2 -mr-1 mydropdown" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
        <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
      </svg>
    </button>
  </div>

<!-- 나오고 사라지는 애니메이션 -->
  <transition
      enter-active-class="transition duration-100 ease-out"
      enter-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-75 ease-in"
      leave-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
  <div v-show="menu" class="absolute right-0 z-10 w-56 mt-2 origin-top-right bg-white divide-y divide-gray-100 rounded-md shadow-lg mydropdown ring-1 ring-black ring-opacity-5 focus:outline-none" role="menu" aria-orientation="vertical" aria-labelledby="menu-button" tabindex="-1">
    <div class="py-1 mydropdown" role="none">
      <!-- Active: "bg-gray-100 text-gray-900", Not Active: "text-gray-700" -->
      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-300" role="menuitem" tabindex="-1" id="menu-item-0" @click.prevent="goProfile">프로필</a>
      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-300" role="menuitem" tabindex="-1" id="menu-item-1" @click.prevent="goUpdate">회원 정보 수정</a>
    </div>
    <div class="py-1 mydropdown" role="none">
      <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-300" role="menuitem" tabindex="-1" id="menu-item-2" @click.prevent="logout">로그아웃</a>
    </div>
  </div>
  </transition>
</div>
</template>

<script>
import {mapState} from 'vuex'
// import axios from 'axios'
export default {
  name: 'Dropdown',
  props: {
    menu: {
      type: Boolean,
    },
    me: {
      type: Object,
    }
  },
  data: function () {
    return {
      username: localStorage.getItem('username'),

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
 
    toggleMenu: function () {
      this.$emit('toggle')
    },
    goUpdate: function () {
      this.$router.push({name:'UserUpdate', params:{username: this.username}})
    },
    logout: function () {
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
      this.$store.dispatch('userLogin', '')
    },
    goProfile: function() {
      this.$router.push({ name: 'Profile', params: {username: this.username}})
    },
  },
  computed: {
    ...mapState([
      'isLogin',
    ]),
    profileImage: function () {
      const img = process.env.VUE_APP_URL.slice(0, -1) + this.me.image_path
      return img
    }
  },
  created: function() {
    this.getProfile()
  }
}
</script>

<style>

</style>