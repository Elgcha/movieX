<template>
<div class="w-full max-w-xs mx-auto my-5">
  <div class="px-8 pt-6 pb-8 mb-4 bg-white rounded shadow-md">
    <div class="mb-4">
      <label for="username" class="block mb-2 text-sm font-bold text-gray-700">Username </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="username" v-model="credentials.username">
    </div>
    <div class="mb-6">
      <label for="password" class="block mb-2 text-sm font-bold text-gray-700">Password </label>
      <input class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 border border-red-500 rounded appearance-none hadow focus:outline-none focus:shadow-outline" type="password" id="password" v-model="credentials.password" >
    </div>

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
      }
    }
  },
  methods: {
    login: function () {
      axios({
        method: 'post',
        url:'http://127.0.0.1:8000/accounts/api-token-auth/',
        data: this.credentials,
      })
        .then(res => {
          // console.log(res)
          localStorage.setItem('jwt', res.data.token)
          localStorage.setItem('username', this.credentials.username)
          this.$emit('login')
          this.$router.push({ name:'Home'})
        })
        .catch(err => {
          console.log(err)
        })
    },
    moveToSignup: function () {
      this.$router.push({name:'Signup'})
    }

  }
}
</script>

<style>

</style>