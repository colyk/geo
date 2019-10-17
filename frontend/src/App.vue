<template>
  <v-app id="app">
      <PathBuilder />
  </v-app>
</template>

<script>
import PathBuilder from './components/PathBuilder.vue';

export default {
  name: 'app',
  components: {
    PathBuilder,
  },
};
</script>

<style>
  html, body {
    overflow-y:hidden;
    height:100%;
  }
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

</style>
