<template>
  <SbcSignout :redirect-url="redirectUrl"></SbcSignout>
</template>

<script>
import SbcSignout from "sbc-common-components/src/components/SbcSignout.vue";

export default {
  props: {
    redirectUrl: {
      default: sessionStorage.getItem("VUE_APP_FRONTEND_DOMAIN"),
      type: String
    }
  },
  data() {
    return {
      redUrl: null
    };
  },
  components: {
    SbcSignout
  }
};
</script>

<style></style>
