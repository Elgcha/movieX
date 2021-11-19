import Vue from 'vue'
import Vuex from 'vuex'
import router from '@/router/'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    isLogin: false,
  },
  mutations: {
    USER_LOGIN: function (state) {
      state.isLogin = true
    },
    USER_LOGOUT: function(state) {
      state.isLogin = false
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
    userLogin: function ({commit}, token) {
      if (token) {
        commit('USER_LOGIN')
      } else {
        commit('USER_LOGOUT')
      }
    }
  },
  modules: {
  }
})
