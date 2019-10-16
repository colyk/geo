<template>
  <div id="app">
    <!--<img alt="Vue logo" src="./assets/logo.png">-->
    <div id="map">
      <Map/>
    </div>
  </div>
</template>

<script>
  import Map from './components/Map.vue';

  export default {
    name: 'app',
    components: {
      Map,
    },
  };
</script>

<style>
  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  #map {
    width: 800px;
    height: 800px;
  }
</style>
