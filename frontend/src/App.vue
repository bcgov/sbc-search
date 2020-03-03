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
import { mapGetters } from "vuex";

import SbcLayout from "sbc-common-components/src/components/SbcLayout.vue";

export default Vue.extend({
  components: {
    SbcLayout
  }
});
</script>

<style lang="scss">
* {
  font-family: "BCSans", "Verdana", "Arial", "sans-serif" !important;
}
.layout-wrapper {
  background-color: #f1f3f6;
}
.app-body {
  margin-top: 0 !important;
}
.cursor-pointer {
  cursor: pointer;
}

.export-btn {
  letter-spacing: 0 !important;
  text-transform: none !important;
  padding: 0 2em !important;
}
</style>
