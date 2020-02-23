<template>
  <v-app>
    <SbcLayout>
      <router-view />
    </SbcLayout>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import "@bcgov/bc-sans/css/BCSans.css";

import SbcLayout from "sbc-common-components/src/components/SbcLayout.vue";

export default Vue.extend({
  components: {
    SbcLayout
  }
});
</script>

<style lang="scss"></style>
