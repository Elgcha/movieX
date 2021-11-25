<template >
<v-parallax src="../../assets/images/login-back.jpg" height="600" class="rounded-md">
<div class="w-full max-w-xs mx-auto my-5">
  <div class="px-8 pt-6 pb-8 mb-4 bg-white rounded shadow-md">
    <div class="mb-4">
      <v-text-field label="username" v-model="credentials.username"></v-text-field>
      <!-- <label for="username" class="block mb-2 text-sm font-bold text-gray-700">Username </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="username" v-model="credentials.username"> -->
    </div>
    <div class="mb-6">
      <v-text-field label="password" type="password" name="password" v-model="credentials.password" @keyup.enter="login"></v-text-field>
      <!-- <label for="password" class="block mb-2 text-sm font-bold text-gray-700">Password </label>
      <input @keyup.enter="login" class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 border border-red-500 rounded appearance-none hadow focus:border-0 focus:outline-none focus:shadow-outline" type="password" id="password" v-model="credentials.password" > -->
    </div>
    <li v-show="errOccur" class="mb-3 text-sm text-black">아이디와 비밀번호를 확인해주세요.</li>

    <div class="flex items-center justify-between">
      <button class="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline" type="button" @click="login">
        Login
      </button>
      <a class="inline-block text-sm font-bold text-blue-500 align-baseline hover:text-blue-800" @click.prevent="moveToSignup" href="#">
        signup
      </a>
    </div>
  </div>
</div>
</v-parallax>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Login',
  data: function () {
    return {
      credentials: {
        username: null,
        password: null,
      },
      errOccur: false,
      image: {backgroundImage: "url(../../assets/images/login-back.jpg)"},
    }
  },
  methods: {
    login: function () {
      const url = process.env.VUE_APP_URL + 'accounts/api-token-auth/'
      axios({
        method: 'post',
        url: url,
        data: this.credentials,
      })
        .then(res => {
          // console.log(res)
          localStorage.setItem('jwt', res.data.token)
          localStorage.setItem('username', this.credentials.username)
          this.$emit('login')
          this.$router.push({ name:'Home'})
        })
        .catch((err) => {
          console.log(err)
          this.errOccur = true
        })
    },
    moveToSignup: function () {
      this.$router.push({name:'Signup'})
    }

  }
}
</script>

<style scoped>
#login-back {
  background: url('../../assets/images/login-back.jpg') no-repeat center center fixed !important;
  background-size: cover;
}
</style>