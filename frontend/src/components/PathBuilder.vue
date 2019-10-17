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
              v-on:right-click="onRightClick"
              :circlesCoords="selectedPoints"
              :lineCoords="selectedPoints"
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
            Selected points:
            <v-list dense>
              <v-list-item
                v-for="(point, index) in selectedPoints"
                :key="index"
                @click=""
              >
                <v-list-item-content>
                  <v-list-item-title>Lat: {{ point[0] }}</v-list-item-title>
                  <v-list-item-title>Lng: {{ point[1] }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
</v-app>
</template>

<script>

import Map from './Map.vue';
import { get_path } from '../Requests.js';

export default {
  name: 'PathBuilder',
  components: {
    Map,
  },
  data() {
    return {
      selectedPoints: [],
    };
  },
  methods: {
    onRightClick({ lat, lng }) {
      this.selectedPoints.push([lat, lng]);
      if (this.selectedPoints.length > 1) {
        get_path()
          .then((result) => { console.log(result); })
          .catch((e) => { console.log(e); });
      }
    },

  },
};
</script>
