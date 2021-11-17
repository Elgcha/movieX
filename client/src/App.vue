<template>
  <div id="app">
    <div id="nav" class="bg-dark bg-opacity-50 d-flex justify-content-between">
      <p class="my-0 text-white">moiveX</p>
      <div>
        <router-link to="/">Home</router-link> |
        <router-link to="/community/">Forum</router-link> |
      </div>
    </div>
    <div class="container">
      <router-view/>
    </div>
    <div id="footer">
      <p>footer</p>
    </div>
  </div>
</template>

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
</style>
