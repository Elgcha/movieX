<template>
  <div>
    
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Profile',
  data: function () {
    return {
      me: {},
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
      axios({
        method: 'get',
        url: `http://127.0.0.1:8000/accounts/profile/`,
        headers: this.setToken(),
      })
        .then(res => {
          this.me = res.data
          console.log(res)
        })
        .catch(err => {
          console.log(err)
        })
    }
  },
  created: function () {
    this.getProfile()
  }
}
</script>

<style>

</style>