<template>
<v-card height="100%">
    <Map width="80%"/>

    <v-navigation-drawer
      absolute
      permanent
      right
      :clipped="true"
    >
      <template v-slot:prepend>
        Added points:
      </template>

      <v-divider></v-divider>

      <v-list dense>

      </v-list>
    </v-navigation-drawer>
  </v-card>
</template>

<script>

import Map from './Map.vue';


export default {
name: 'PathBuilder',
  components: {
    Map,
  },
  data() {
    return {

    };
  },
  methods: {

  },
};
</script>
