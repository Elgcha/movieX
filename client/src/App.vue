<template>
  <div id="app">
    <div id="nav" class="flex justify-between bg-gray-400">
      <p class="my-0 text-white">moiveX</p>
      <div>
        <router-link to="/">Home</router-link> |
        <router-link to="/community/forum/">Forum</router-link> |
        <router-link to="/movies/">Movies</router-link> |
        <span v-if="isLogin">
          <router-link to="/accounts/profile/">profile</router-link> |
          <router-link @click.native="logout" to='#'>logout</router-link> |
        </span>
        <span v-else>
          <router-link to="/accounts/login/">Login</router-link> |
          <router-link to="/accounts/signup/">signup</router-link> |
        </span>
        <a href="http://127.0.0.1:8000/admin">Admin</a> |
      </div>
    </div>
    <div class="container px-4 mx-auto">
      <router-view @login="isLogin=true"/>
    </div>
    <div id="footer">
      <p>footer</p>
    </div>
  </div>
</template>

<script>

export default ({
  name: 'App',
  data: function () {
    return {
      isLogin: false,
    }
  },
  methods: {
    logout: function () {
      this.isLogin = true
      localStorage.removeItem('jwt')
      this.$router.push({ name: 'Login' })
    },
    
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

body {
  background-color: rgba(61, 26, 26, 0.568);
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
