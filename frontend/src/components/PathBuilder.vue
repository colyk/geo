<template>
<v-app>
    <v-container class="grey lighten-5 pa-0" fluid>
      <v-row no-gutters>
        <v-col
          cols="9"
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
          cols="3"
        >
          <v-card
            outlined
            tile
          >
            Selected points:
            <v-list dense>
              <v-list-item
                v-for="(point, index) in pointsInfo"
                :key="index"
                @contextmenu.prevent="$refs.menu.open($event, {point, index})"
              >
                <v-list-item-content>
                  <v-list-item-title>{{ point.name }}</v-list-item-title>
                  <v-list-item-subtitle >Lat: {{ point.lat }}</v-list-item-subtitle>
                  <v-list-item-subtitle >Lon: {{ point.lon }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
              <v-list-item v-if="pathLength">
                <v-list-item-content>
                  <v-list-item-title>Length of the path: </v-list-item-title>
                  <v-list-item-subtitle >{{ pathLength }}</v-list-item-subtitle>
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
import { fetchPath, getInfoByCoord } from '../Requests';
import { hasCoords } from '../utils';

function degreesToRadians(degrees) {
  return degrees * Math.PI / 180;
}

function distance(coord1, coord2) {
  let [lat1, lon1] = coord1;
  let [lat2, lon2] = coord2;
  const earthRadiusKm = 6371;

  const dLat = degreesToRadians(lat2 - lat1);
  const dLon = degreesToRadians(lon2 - lon1);

  lat1 = degreesToRadians(lat1);
  lat2 = degreesToRadians(lat2);

  const a = Math.sin(dLat / 2) * Math.sin(dLat / 2)
          + Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(lat1) * Math.cos(lat2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return earthRadiusKm * c;
}

export default {
  name: 'PathBuilder',
  components: {
    Map,
    VueContext,
  },
  data() {
    return {
      selectedPoints: [],
      pointsInfo: [],
      lineCoords: [],
      clickedOnPoint: null,
      geojson: null,
      pathLength: null,
    };
  },
  methods: {
    onClick(type) {
      if (type === 'remove') {
        this.selectedPoints.splice(this.clickedOnPoint.index, 1);
        this.pointsInfo.splice(this.clickedOnPoint.index, 1);
        this.lineCoords = [];
        this.pathLength = null;
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
        this.addPointInfo(lat, lng);
        this.selectedPoints.push([lat, lng]);

        this.requestPath();
      }
    },
    requestPath() {
      if (this.selectedPoints.length > 1) {
        fetchPath(this.selectedPoints)
          .then((result) => {
            const { path } = result.data;
            let pathLength = 0;
            for (let i = 0; i < path.length - 1; i++) pathLength += distance(path[i], path[i + 1]);
            this.lineCoords = path;
            this.pathLength = `${pathLength.toFixed(3)} km`;
          })
          .catch((e) => { console.log(e); });
      }
    },
    addPointInfo(lat, lon) {
      getInfoByCoord(lat, lon)
        .then(({ data }) => {
          const info = { lat: Number(data.lat).toFixed(7), lon: Number(data.lon).toFixed(7), name: data.display_name };
          console.log(info);
          this.pointsInfo.push(info);
        })
        .catch((e) => {
          const info = { lat, lon, name: '-' };
          this.pointsInfo.push(info);
          console.log(e);
        });
    },

  },
};
</script>

<style>
.v-context { padding:0!important;}
</style>
