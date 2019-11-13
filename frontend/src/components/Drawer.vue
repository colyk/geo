<template>
<v-app>
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
              :showDrawToolbar="true"
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
            Drawn objects:
            <v-list dense>

            </v-list>
          </v-card>

        </v-col>
      </v-row>
    </v-container>
</v-app>
</template>

<script>

import Map from './Map.vue';
import GeoJSON from '../geojson';

export default {
  name: 'Drawer',
  components: {
    Map,
  },
  data() {
    return {
    };
  },

};
</script>

<style>
.v-context { padding:0!important;}
</style>
