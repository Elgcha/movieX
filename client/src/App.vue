<template >
  <div id="app" @click="offMenu" class="text-gray-200">
    <div id="nav" class="flex w-full p-2 bg-black">
      <img src="@/assets/images/logo.png" @click="moveToMain" alt="" class="w-1/12 cursor-pointer">
      <!-- <p class="pl-2 my-auto text-2xl text-white cursor-pointer font-jalnan" @click="moveToMain">moiveX</p> -->
      <div v-if="isLogin" class="w-9/12 my-auto ml-3 text-left text-gray-400">
        <router-link class="mx-2 hover:text-gray-200" to="/">Main</router-link>
        <router-link class="mx-2 hover:text-gray-200" to="/community/forum/">Forum</router-link>
        <router-link class="mx-2 hover:text-gray-200" to="/movies/">Search</router-link>
        <router-link class="mx-2 hover:text-gray-200" to="/movies/add/search/">Add</router-link>
        <!-- <a href="http://127.0.0.1:8000/admin">Admin</a> -->
      </div>
      <div class="flex ml-auto">
        <movie-eval class="mx-2 my-auto bg-gray-800 rounded" v-if="isLogin"></movie-eval>
        <accounts-dropdown :menu="menu" :me="me" @toggle="toggleMenu" class="ml-3 mydropdown" v-if="isLogin"></accounts-dropdown>
        <span v-else class="my-auto ml-auto">
          <router-link to="/accounts/login/" class="btn btn-blue">Login</router-link>
        </span>
      </div>
    </div>
    <div class="container px-4 py-4 mx-auto bg-black rounded">
      <router-view @login="login"/>
    </div>
    <!-- <div id="footer">
      <p>footer</p>
    </div> -->
  </div>
</template>

<script>
import {mapState} from 'vuex'
import accountsDropdown from '@/components/Home/accountsDropdown.vue'
import movieEval from '@/components/movies/movieEval.vue'
import axios from 'axios'
export default ({
  name: 'App',
  components: {
    accountsDropdown,
    movieEval
  },
  data: function () {
    return {
      username: localStorage.getItem('username'),
      menu: false,
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
      const url = process.env.VUE_APP_URL + `accounts/profile/get/self/`
      axios({
        method: 'get',
        url: url,
        headers: this.setToken(),
      })
        .then(res => {
          this.me = res.data
        })
        .catch(err => {
          console.log(err)
        })
    },
    moveToMain: function () {
      if (this.isLogin) {
        this.$router.push({name:'Home'})
      }
    },
    offMenu: function (event) {
      if (!event.target.classList.contains('mydropdown')){
        this.menu = false
      }

    },
    toggleMenu: function() {
      this.menu = !this.menu
    },
    logout: function () {
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
      this.$store.dispatch('userLogin', '', '')
    },
    login: function () {
      const token = localStorage.getItem('jwt')
      if (token) {
        const username = localStorage.getItem('username')
        this.$store.dispatch('userLogin', token, username)
      } else {
        this.$router.push({name:'Login'})
      }
    },
    goProfile: function() {
      this.$router.push({ name: 'Profile', params: {username: this.username}})
    },
    
  },
  created: function () {
    this.login()
    this.getProfile()
  },
  computed: {
    ...mapState([
      'isLogin',
    ]),
  },
})
</script>

<style>


#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
}

#nav a {
  font-weight: bold;
}

#nav a.router-link-exact-active {
  /* color: #84b9a2; */
  @apply text-gray-50
}



#footer {
  background-color: black;
  color: white;
  padding: 10px;
}

.btn {
  @apply font-bold py-2 px-4 rounded;
}
.btn-blue {
  @apply bg-gray-500 text-white;
}
.btn-blue:hover {
  @apply bg-gray-700;
}

</style>
