<template>
  <v-app >
    <l-map
      ref="map"
      @contextmenu="onContextMenu"
      :zoom="zoom"
      :center="center"
      :zoomAnimation="true"
      :markerZoomAnimation="true"
      :fadeAnimation="true"
      :inertia="true"
      :inertiaMaxSpeed="50"
      :inertiaDeceleration="200"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <l-tile-layer :url="url" :attribution="attribution"></l-tile-layer>
      <l-marker v-if="markerLatLng" :lat-lng="markerLatLng" ></l-marker>
      <l-circle
        v-if="circlesCoords.length"
        v-for="(coord, id) in circlesCoords"
        :key="id"
        :lat-lng="coord"
        :radius="circleRadius"
        color="#eb346bcc"
      />
      <l-polyline
        v-if="lineCoords.length"
        :lat-lngs="lineCoords"
        color="#55eb34cc">
      </l-polyline>
      <l-control position="bottomleft">
       <v-btn small class="map_btn" @click="showCurLoc">My location</v-btn>
     </l-control>
      <l-control v-if="geojson" position="bottomleft">
       <v-btn small class="map_btn" @click="showGeojsonAtCenter">Center geoJson data</v-btn>
     </l-control>
      <v-geosearch :options="geosearchOptions" ></v-geosearch>
      <l-control-polyline-measure :options="{ showUnitControl: false }" position="bottomright"/>
      <l-geo-json
        :geojson="geojson"
        ref="geojson"
      >
      </l-geo-json>
    </l-map>
  </v-app>
</template>

<script>
import { OpenStreetMapProvider } from 'leaflet-geosearch';
import VGeosearch from 'vue2-leaflet-geosearch';
import { getCurrentPosition } from '../utils';

export default {
  name: 'Map',
  components: { VGeosearch },
  props: {
    circlesCoords: { type: Array, default: () => [] },
    lineCoords: { type: Array, default: () => [] },
    geojson: { type: Object, default: null },
  },
  data() {
    return {
      // https://leaflet-extras.github.io/leaflet-providers/preview/
      url: 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',
      zoom: 12,
      circleRadius: 400,
      center: [51.2477870, 22.570132],
      bounds: null,
      markerLatLng: null,
      attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      geosearchOptions: {
        provider: new OpenStreetMapProvider(),
        // autoClose: true,
        showPopup: true,
      },
    };
  },
  mounted() {},
  methods: {
    showCurLoc() {
      getCurrentPosition().then(({ coords }) => {
        this.center = [coords.latitude, coords.longitude];
        this.zoom = 11;
        this.markerLatLng = this.center;
        console.log(this.center);
      });
    },
    showGeojsonAtCenter() {
      this.bounds = this.$refs.geojson.getBounds();
      this.$refs.map.fitBounds(this.bounds);
    },
    onContextMenu(e) {
      this.$emit('right-click', e.latlng);
    },
    zoomUpdated(zoom) {
      this.zoom = zoom; // from 0 to 18
      this.circleRadius = 1145 - (this.zoom + 1) * 60;
    },
    centerUpdated(center) {
      this.center = center;
    },
    boundsUpdated(bounds) {
      this.bounds = bounds;
    },
  },
};
</script>

<style>
  .map_btn {
    background-color: #fff!important;
    text-transform: capitalize!important;
  }
</style>
