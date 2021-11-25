<template>
<v-parallax src="../../assets/images/login-back.jpg" height="700" class="rounded-md">
<div class="w-full max-w-xs mx-auto my-5">
  <div class="px-8 pt-6 pb-8 mb-4 bg-white rounded shadow-md">
    <div class="text-xl text-black">Signup</div>
    <div class="mb-4">
      <v-text-field label="username" v-model="credentials.username"></v-text-field>
      <!-- <label for="username" class="block mb-2 text-sm font-bold text-gray-700">Username </label>
      <input class="w-full px-3 py-2 leading-tight text-gray-700 border rounded shadow appearance-none focus:outline-none focus:shadow-outline" type="text" id="username" v-model="credentials.username"> -->
    </div>
    <div class="mb-4">
      <v-text-field label="email" v-model="credentials.email"></v-text-field>
      <!-- <label for="email" class="block mb-2 text-sm font-bold text-gray-700">Email </label>
      <input class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 border rounded appearance-none hadow focus:outline-none focus:shadow-outline" type="text" id="email" v-model="credentials.email" > -->
    </div>
    <div class="mb-4">
      <v-text-field label="password" type="password" name="password" v-model="credentials.password"></v-text-field>
      <!-- <label for="password" class="block mb-2 text-sm font-bold text-gray-700">Password </label>
      <input class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 border border-red-500 rounded appearance-none hadow focus:outline-none focus:shadow-outline" type="password" id="password" v-model="credentials.password" > -->
    </div>
    <div class="mb-6">
      <v-text-field label="passwordConfirmation" type="password" name="password" v-model="credentials.passwordConfirmation" @keyup.enter="signup"></v-text-field>
      <!-- <label for="passwordConfirmation" class="block mb-2 text-sm font-bold text-gray-700">PasswordConfirmation </label>
      <input 
      type="password" 
      id="passwordConfirmation" 
      v-model="credentials.passwordConfirmation"
      @keyup.enter="signup"
      class = "w-full px-3 py-2 mb-3 leading-tight text-gray-700 border border-red-500 rounded appearance-none hadow focus:outline-none focus:shadow-outline"
      > -->
    </div>
    <div v-if="errorMessage" class="mb-3 text-red-600">{{ errorMessage }}</div>
    <button @click="signup" class="px-4 py-2 font-bold text-white bg-blue-500 rounded hover:bg-blue-700 focus:outline-none focus:shadow-outline">회원가입</button>
  </div>
</div>
</v-parallax>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Signup',
  data: function () {
    return {
      credentials: {
        username: null,
        email: null,
        password: null,
        passwordConfirmation: null,
      },
      errorMessage: null,
    }
  },
  methods: {
    signup: function () {
      const url = process.env.VUE_APP_URL + 'accounts/signup/'
      axios({
        method: 'post',
        url: url,
        data: this.credentials
      })
        .then(res => {
          console.log(res.data.error)
          if (res.data.error) {
            this.errorMessage = res.data.error
          } else {
            this.$router.push({ name: 'Login'})
          }
        })
        .catch(err => {
          console.log(err.data)
        })
    }
  }
}
</script>
