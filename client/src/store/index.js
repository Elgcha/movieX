import Vue from 'vue'
import Vuex from 'vuex'
import router from '@/router/'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
  },
  mutations: {
  },
  actions: {
    moveToDetail: function (context, moviePk) {
      router.push({ name: 'MovieDetail', params: {moviePk: moviePk}})
    },
    setToken: function () {
      const token = localStorage.getItem('jwt')
      const config = {
        Authorization: `JWT ${token}`
      }
      return config
    },
  },
  modules: {
  }
})
