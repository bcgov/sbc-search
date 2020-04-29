<template>
  <v-btn
    :type="type"
    color="primary outline font-16"
    height="56"
    class="sbc-button"
    :elevation="0"
    :loading="disabled"
    :disabled="disabled"
    :block="$vuetify.breakpoint.xsOnly"
    >{{ title }}</v-btn
  >
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
    },
    disabled: {
      default: false,
      type: Boolean
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
