<template>
  <div></div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'MovieList',
  methods: {
    getMovies: function() {
      axios({
        methods: 'get',
        url: 'http://127.0.0.1:8000/movies/',
      })
        .then(res => {
          console.log(res)
        })
    }
  },
  created: function () {
    this.getMovies()
  }
}
</script>

<style>

</style>