<template>
<v-app>
    <v-container class="grey lighten-5" fluid>
      <v-row no-gutters>
        <v-col
          cols="1"
          sm="10"
        >
          <v-card
            outlined
            tile
          >
            <Map
              :geojson="geojson"
            />
          </v-card>
        </v-col>
        <v-col
          cols="2"
          sm="2"
        >
          <v-card
            outlined
            tile
          >
            <v-file-input label="File input" @change="drawGeojson"></v-file-input>

          </v-card>

        </v-col>
      </v-row>
    </v-container>
</v-app>
</template>

<script>

import Map from './Map.vue';
import { fetchPath } from '../Requests';

export default {
  name: 'GeoJsonDrawer',
  components: {
    Map,
  },
  data() {
    return {
      geojson: null,
    };
  },
  methods: {
    drawGeojson(file) {
      console.log(file)
      const reader = new FileReader();
reader.onload = e => this.geojson = JSON.parse(e.target.result);

reader.readAsText(file);
    },
  },
};
</script>

<style>
.v-context { padding:0!important;}
</style>
