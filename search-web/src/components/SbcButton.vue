<template>
  <v-btn :type="type" color="primary outline" height="50" class="sbc-button">{{
    title
  }}</v-btn>
</template>

<script>
export default {
  props: {
    title: {
      default: null,
      type: String
    },
    type: {
      default: null,
      type: String
    }
  }
};
</script>

<style lang="scss">
.sbc-button {
  text-transform: none !important;
  letter-spacing: 0 !important;
  width: 125px !important;
}
</style>
