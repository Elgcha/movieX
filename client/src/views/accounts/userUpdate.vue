<template>
  <div class="p-2 text-white bg-gray-800">
    <label for="profileUpload" class="text-xl">프로필 수정</label>
    <div class="flex">
      <div class="md:w-3/12 md:ml-16">
        <!-- profile image -->
        <img class="object-cover w-20 h-20 p-1 border-2 border-pink-600 rounded-full md:w-40 md:h-40" :src="profileImage" alt="profile">
      </div>
      <!-- 프로필 수정 -->
      <div class="my-auto">
        <input type="file" name="" id="profileUpload" @change="imageUpload" ref="profileImage" class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none focus:border-transparent">
        <div class="mt-3">파일을 선택하면 자동으로 업로드 됩니다.</div>
      </div>
    </div>
    <div class="mb-4">
      <label for="username" class="block mb-2 text-sm font-bold text-white">Email </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 bg-white border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="username" v-model="email">
      <div v-if="errorMessage" class="mb-3 text-red-600">{{ errorMessage }}</div>
      <button @click="emailUpdate" class="m-2 ml-auto btn btn-blue">이메일 수정</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'UserUpdate',
  data: function () {
    return {
      me: {},
      file: null,
      email: null,
      errorMessage: null,
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
    getProfile: function () {
      const username = this.$route.params.username
      const url = process.env.VUE_APP_URL + `accounts/profile/${username}/`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.me = res.data
          this.email = this.me.email
        })
        .catch(err => {
          console.log(err)
        })
    },
    imageUpload: function (event) {
      const username = this.$route.params.username
      const token = localStorage.getItem('jwt')
      this.file = event.target.files[0]
      if (this.file) {
        let data = new FormData()
        data.append('image', this.file)
        const url = process.env.VUE_APP_URL + `accounts/profiles/${username}/`
        axios({
          method: 'put',
          url: url,
          data: data,
          headers: {
            'Content-Type': 'multipart/form-data',
            Authorization: `JWT ${token}`
          },
        })
          .then(() => {
            this.getProfile()
          })
          .catch(err => {
            console.log(err)
          })
      }
    },
    emailUpdate: function () {
      const url = process.env.VUE_APP_URL + `accounts/${this.me.username}/update/`
      axios({
        method: 'put',
        url: url,
        data: {
          'email': this.email,
        },
        headers: this.setToken(),
      })
        .then(res => {
          if (res.data.error) {
            this.errorMessage = res.data.error
          } else {
            this.getProfile()
            this.errorMessage = null
          }
        })
        .catch(err => {
          console.log(err.data)
        })
    }
  },
  created: function () {
    this.getProfile()
  },
  computed: {
    profileImage: function () {
      const img = process.env.VUE_APP_URL.slice(0, -1) + this.me.image_path
      return img
    },
  }
  
}
</script>

<style>
input[type=file]::-webkit-file-upload-button,
input[type=file]::file-selector-button {
    @apply text-white bg-gray-700 hover:bg-gray-600 font-medium text-sm cursor-pointer border-0 py-2.5 pl-8 pr-4;
    margin-inline-start: -1rem;
    margin-inline-end: 1rem;
}
</style>