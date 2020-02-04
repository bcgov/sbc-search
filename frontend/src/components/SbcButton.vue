<template>
  <div class="d-inline-block">
    <v-btn
      v-if="variant === 1"
      depressed
      x-large
      color="primary"
      class="sbc-btn font-weight-regular"
      :height="height"
      :width="width"
      :disabled="disabled"
      >{{ title }}</v-btn
    >
    <v-btn
      v-if="variant === 2"
      outlined
      x-large
      class="sbc-btn sbc-btn-clear font-weight-regular"
      :height="height"
      :disabled="disabled"
      :width="width"
      >{{ title }}</v-btn
    >
  </div>
</template>

<script>
export default {
  props: {
    title: {
      default: "",
      type: String
    },
    height: {
      default: 59,
      type: Number
    },
    width: {
      default: null,
      type: Number
    },
    variant: {
      default: 1,
      type: Number
    },
    disabled: {
      default: false,
      type: Boolean
    }
  }
};
</script>

<style lang="sass">
.v-application .sbc-btn
    font-size: 0.9em !important
    text-transform: none
    letter-spacing: 0.5px

.v-application .sbc-btn-clear
    color: $COLOR_SECONDARY !important
    border: 1px solid $COLOR_GREY
</style>
