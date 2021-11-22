import Vue from 'vue'
import Vuex from 'vuex'
import router from '@/router/'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLogin: false,
    username: null,
  },
  mutations: {
    USER_LOGIN: function (state, username) {
      state.isLogin = true
      state.username = username
    },
    USER_LOGOUT: function(state) {
      state.isLogin = false
      state.username = null
    }
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
    userLogin: function ({commit}, token, username) {
      if (token) {
        commit('USER_LOGIN', username)
      } else {
        commit('USER_LOGOUT')
      }
    }
  },
  modules: {
  }
})
