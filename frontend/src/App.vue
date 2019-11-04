<template>
  <v-app id="app">
    <v-card height="100%">
      <v-navigation-drawer
        expand-on-hover
        permanent
        absolute
        id="nav"
      >

        <v-list
          nav
          dense
        >
          <v-list-item @click="onItemClick('build_path')" :class="{ 'blue-grey lighten-4': drawPathBuilder }">
            <v-list-item-icon>
              <v-icon>mdi-map-marker-radius</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Build path</v-list-item-title>
          </v-list-item>
          <v-list-item @click="onItemClick('geojson')" :class="{ 'blue-grey lighten-4': drawGeoJsonViewer }">
            <v-list-item-icon>
              <v-icon>mdi-map</v-icon>
            </v-list-item-icon>
            <v-list-item-title>GeoJson viewer</v-list-item-title>
          </v-list-item>

          <v-list-item @click="onItemClick('drawer')" :class="{ 'blue-grey lighten-4': drawDrawer }">
            <v-list-item-icon>
              <v-icon>mdi-draw</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Geo drawer</v-list-item-title>
          </v-list-item>

        </v-list>
      </v-navigation-drawer>
        <PathBuilder v-if="drawPathBuilder" class="maps"/>
        <GeoJsonViewer v-if="drawGeoJsonViewer" class="maps"/>
        <Drawer v-if="drawDrawer" class="maps"/>
    </v-card>

  </v-app>
</template>

<script>
import PathBuilder from './components/PathBuilder.vue';
import GeoJsonViewer from './components/GeoJsonViewer';
import Drawer from './components/Drawer';

export default {
  name: 'app',
  components: {
    GeoJsonViewer,
    PathBuilder,
    Drawer,
  },
  data() {
    return {
      drawPathBuilder: true,
      drawGeoJsonViewer: false,
      drawDrawer: false,
    };
  },

  methods: {
    onItemClick(type) {
      this.hideAllMaps();
      if (type === 'build_path') this.drawPathBuilder = true;
      if (type === 'geojson') this.drawGeoJsonViewer = true;
      if (type === 'drawer') this.drawDrawer = true;
    },
    hideAllMaps() {
      this.drawPathBuilder = false;
      this.drawDrawer = false;
      this.drawGeoJsonViewer = false;
    },
  },
};
</script>

<style>
  html, body {
    overflow-y: hidden;
    overflow-x: hidden;
    height: 100%;
  }

  #app {
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
  }

  .maps {
    margin-left: 72px;
  }

  #nav {
    z-index:2000;
  }

</style>
