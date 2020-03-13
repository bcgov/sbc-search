<template>
  <SbcSignout :redirect-url="redirectUrl"></SbcSignout>
</template>

<script>
import SbcSignout from "sbc-common-components/src/components/SbcSignout.vue";

export default {
  props: {
    redirectUrl: {
      default: "/",
      type: String
    }
  },
  components: {
    SbcSignout
  }
};
</script>

<style></style>
