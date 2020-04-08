<template>
  <v-btn
    class="add-filter-button sbc-button text-capitalize body-1 color-dark-grey border-gray"
    outlined
    height="50"
    :elevation="0"
  >
    <v-icon left>add</v-icon>
    {{ title }}
  </v-btn>
</template>

<script>
export default {
  props: {
    title: {
      default: null,
      type: String
    }
  }
};
</script>

<style lang="scss"></style>
