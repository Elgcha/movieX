<template>
  <div>
    <img :src="'https://image.tmdb.org/t/p/w500/' + people.profile_path" alt="">
    {{ people.also_known_as[1] }}
    
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'PeopleDetail',
  data: function () {
    return {
      people: {},
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
    getPeople: function () {
      const url = process.env.VUE_APP_URL + `movies/people/${this.$route.params.peoplePk}`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.people = res.data
        })
    },
  },
  created: function () {
    this.getPeople()
  },
  computed: {
    
  }
}
</script>

<style>

</style>