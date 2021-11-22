<template >
  <div id="app" @click="offMenu">
    <div id="nav" class="flex justify-between bg-gray-400">
      <p class="my-0 text-white">moiveX</p>
      <div>
        <router-link to="/">Home</router-link> |
        <router-link to="/community/forum/">Forum</router-link> |
        <router-link to="/movies/">Search</router-link> |
        <a href="http://127.0.0.1:8000/admin">Admin</a>
      </div>
      <div>
        <accounts-dropdown :menu="menu" @toggle="toggleMenu" class="mydropdown" v-if="isLogin"></accounts-dropdown>
        <span v-else>
          <router-link to="/accounts/login/">Login</router-link>
        </span>
      </div>
    </div>
    <div class="container px-4 mx-auto">
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

export default ({
  name: 'App',
  components: {
    accountsDropdown,
  },
  data: function () {
    return {
      username: localStorage.getItem('username'),
      menu: false,
    }
  },
  methods: {
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
      this.$store.dispatch('userLogin', '')
    },
    login: function () {
      const token = localStorage.getItem('jwt')
      this.$store.dispatch('userLogin', token)
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
  color: #2c3e50;
}

#nav {
  padding: 10px;
}

#nav a {
  font-weight: bold;
  color: #2c3e50;
}

#nav a.router-link-exact-active {
  color: #84b9a2;
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
