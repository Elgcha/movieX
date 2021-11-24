<template >
  <div id="app" @click="offMenu" class="dark:text-gray-200">
    <div id="nav" class="flex justify-between p-2 bg-gray-500">
      <p class="my-auto text-2xl text-white cursor-pointer" @click="moveToMain">moiveX</p>
      <div v-if="isLogin" class="mx-auto my-auto">
        <router-link to="/">Main</router-link> |
        <router-link to="/community/forum/">Forum</router-link> |
        <router-link to="/movies/">Search</router-link> |
        <router-link to="/movies/add/search/">Add</router-link> |
        <a href="http://127.0.0.1:8000/admin">Admin</a>
      </div>
      <div class="flex">
        <movie-eval class="p-1 mx-2 my-auto bg-gray-400 rounded hover:bg-gray-600" v-if="isLogin"></movie-eval>
        <accounts-dropdown :menu="menu" @toggle="toggleMenu" class="mydropdown " v-if="isLogin"></accounts-dropdown>
        <span v-else class="my-auto">
          <router-link to="/accounts/login/">Login</router-link>
        </span>
      </div>
    </div>
    <div class="container px-4 py-4 mx-auto rounded dark:bg-gray-800">
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
    }
  },
  methods: {
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
  @apply text-green-400
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
  @apply bg-blue-500 text-white;
}
.btn-blue:hover {
  @apply bg-blue-700;
}
</style>
