<template>
  <div style="height: 100%; width: 100%">
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
    </l-map>
  </div>


</template>

<script>
import { getCurrentPosition } from '../utils';

export default {
  name: 'Map',
  data() {
    return {
      // https://wiki.openstreetmap.org/wiki/Tile_servers
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
      console.log(e.latlng);
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
