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
  @import url('https://fonts.googleapis.com/css?family=Roboto:100,300,400,500,700,900|Material+Icons');
  * {
    font-family: 'Roboto', sans-serif;
  }
  body {
    overflow-y: hidden;
  }
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

</style>
