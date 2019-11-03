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
              v-on:right-click="onRightClick"
              :circlesCoords="selectedPoints"
              :lineCoords="lineCoords"
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
            Selected points:
            <v-list dense>
              <v-list-item
                v-for="(point, index) in selectedPoints"
                :key="index"
                @contextmenu.prevent="$refs.menu.open($event, {point, index})"
              >
                <v-list-item-content>
                  <v-list-item-title>Lat: {{ point[0] }}</v-list-item-title>
                  <v-list-item-title>Lng: {{ point[1] }}</v-list-item-title>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card>
        <vue-context ref="menu" @close="onClose" @open="onOpen">
          <v-list dense>
            <v-list-item @click.prevent="onClick('remove')">
              <v-list-item-content>
                Remove
              </v-list-item-content>
            </v-list-item>
          </v-list>
        </vue-context>
        </v-col>
      </v-row>
    </v-container>
</v-app>
</template>

<script>

import { VueContext } from 'vue-context';
import Map from './Map.vue';
import { fetchPath } from '../Requests';
import { hasCoords } from '../utils';

export default {
  name: 'PathBuilder',
  components: {
    Map,
    VueContext,
  },
  data() {
    return {
      selectedPoints: [],
      lineCoords: [],
      clickedOnPoint: null,
      geojson: null,
    };
  },
  methods: {
    onClick(type) {
      if (type === 'remove') {
        this.selectedPoints.splice(this.clickedOnPoint.index, 1);
        this.lineCoords = [];
        this.requestPath();
      }
    },
    onOpen(e, data) {
      this.clickedOnPoint = data;
    },
    onClose(data) {
    },
    onRightClick({ lat, lng }) {
      if (!hasCoords(this.selectedPoints, [lat, lng])) {
        this.selectedPoints.push([lat, lng]);
        this.requestPath();
      }
    },
    requestPath() {
      if (this.selectedPoints.length > 1) {
        fetchPath(this.selectedPoints)
          .then((result) => {
            this.lineCoords = result.data.path;
          })
          .catch((e) => { console.log(e); });
      }
    },

  },
};
</script>

<style>
.v-context { padding:0!important;}
</style>
