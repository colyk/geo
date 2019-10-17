<template>
  <v-app >
    <l-map
      @contextmenu="onContextMenu"
      :zoom="zoom"
      :center="center"
      @update:zoom="zoomUpdated"
      @update:center="centerUpdated"
      @update:bounds="boundsUpdated"
    >
      <l-tile-layer :url="url"></l-tile-layer>
      <l-marker v-if="markerLatLng" :lat-lng="markerLatLng" ></l-marker>
      <l-circle
        v-if="circlesCoords.length"
        v-for="(coord, id) in circlesCoords"
        :key="id"
        :lat-lng="coord"
        :radius="450"
        color="red"
      />
      <l-polyline
        v-if="lineCoords.length"
        :lat-lngs="lineCoords"
        color="green">
      </l-polyline>
    </l-map>
  </v-app>
</template>

<script>
import { getCurrentPosition } from '../utils';

export default {
  name: 'Map',
  props: {
    circlesCoords: { type: Array, default: () => [] },
    lineCoords: { type: Array, default: () => [] },
  },
  data() {
    return {
      // https://wiki.openstreetmap.org/wiki/Tile_servers
      // https://maps.wikimedia.org/osm-intl/${z}/${x}/${y}.png
      url: 'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      zoom: 11,
      center: [47.413220, -1.219482],
      bounds: null,
      markerLatLng: null,
    };
  },
  mounted() {
    getCurrentPosition().then(({ coords }) => {
      this.center = [coords.latitude, coords.longitude];
      this.markerLatLng = this.center;
    });
  },
  methods: {
    onContextMenu(e) {
      this.$emit('right-click', e.latlng);
      console.log(this.lineCoords);
    },
    zoomUpdated(zoom) {
      this.zoom = zoom;
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
