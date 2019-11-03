<template>
<v-app>
        <v-alert
        id="alert"
        dense
        outlined
        type="error"
        transition="slide-y-transition"
        :value="!!alert"
        dismissible
        :min-width="400"
      >
        {{alert}}
      </v-alert>
    <v-container class="grey lighten-5 pa-0" fluid>
      <v-row no-gutters>
        <v-col
          cols="10"
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
  name: 'GeoJsonViewer',
  components: {
    Map,
  },
  data() {
    return {
      geojson: null,
      alert: null
    };
  },
  methods: {
    drawGeojson(file) {
      if (!file){
        this.geojson = null;
        this.alert = null;
        }
      else {
        const reader = new FileReader();
        reader.onload = e => {
        try {
          this.geojson = JSON.parse(e.target.result);
          this.alert = null;
          }
        catch(e) {
            this.alert = "Bad file"
          }
        };
        reader.readAsText(file);
      }
    },
  },
};
</script>

<style>
.v-context { padding:0!important;}

#alert {
  position: absolute;
  z-index: 10000;
  background-color: #fff!important;
  margin-left: 80px;
}
</style>
