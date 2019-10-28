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
          <v-list-item @click="onItemClick('build_path')">
            <v-list-item-icon>
              <v-icon>mdi-map-marker-radius</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Build path</v-list-item-title>
          </v-list-item>
          <v-list-item @click="onItemClick('geojson')">
            <v-list-item-icon>
              <v-icon>mdi-map</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Draw GeoJson</v-list-item-title>
          </v-list-item>

        </v-list>
      </v-navigation-drawer>

            <PathBuilder v-if="drawPathBuilder" class="maps"/>
            <GeoJsonDrawer v-if="drawGeoJsonDrawer" class="maps"/>


    </v-card>

  </v-app>
</template>

<script>
import PathBuilder from './components/PathBuilder.vue';
import GeoJsonDrawer from './components/GeoJsonDrawer';

export default {
  name: 'app',
  components: {
    GeoJsonDrawer,
    PathBuilder,
  },
  data() {
    return {
      drawPathBuilder: false,
      drawGeoJsonDrawer: true,
    };
  },

  methods: {
    onItemClick(type) {
      if (type === 'build_path') {
        this.drawPathBuilder = true;
        this.drawGeoJsonDrawer = false;
      } else {
        this.drawPathBuilder = false;
        this.drawGeoJsonDrawer = true;
      }
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
    margin-left: 60px;
  }

  #nav {
    z-index:2000;
  }

</style>
