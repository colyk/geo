import Vue from 'vue';

import {
  LMap, LTileLayer, LMarker, LCircle, LPolyline, LControl, LGeoJson,
} from 'vue2-leaflet';
import LControlPolylineMeasure from 'vue2-leaflet-polyline-measure';
import { Icon } from 'leaflet';
import App from './App.vue';
import 'leaflet/dist/leaflet.css';
import vuetify from './plugins/vuetify';

Vue.component('l-map', LMap);
Vue.component('l-tile-layer', LTileLayer);
Vue.component('l-marker', LMarker);
Vue.component('l-circle', LCircle);
Vue.component('l-polyline', LPolyline);
Vue.component('l-control', LControl);
Vue.component('l-control-polyline-measure', LControlPolylineMeasure);
Vue.component('l-geo-json', LGeoJson);

delete Icon.Default.prototype._getIconUrl;

Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

Vue.config.productionTip = false;

new Vue({
  vuetify,
  render: h => h(App),
}).$mount('#app');
