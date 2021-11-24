<template>
  <div>
    <img :src="mainMovie.backdop_path" alt="">
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MainTop',
  data: function () {
    return {
      mainMovie: {},
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
    getRandomMovie: function () {
      const url = process.env.VUE_APP_URL + `movies/대문/`

      axios({
        method: 'get',
        url: url,
      })
        .then(res => {
          this.mainMovie = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
  },
  created: function() {
    this.getRandomMovie()
  }
}
</script>

<style>

</style>