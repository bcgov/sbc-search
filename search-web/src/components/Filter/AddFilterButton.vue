<template>
  <v-btn class="add-filter-button sbc-button" height="50">
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
