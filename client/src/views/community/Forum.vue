<template>
  <div>
    <button @click="ArticleCreate">글 작성</button>
  </div>
</template>

<script>
export default {
  name: 'Forum',
  methods: {
    ArticleCreate: function () {
      this.$router.push({name: 'ArticleCreate'})
    }
  }
}
</script>

<style>

</style>