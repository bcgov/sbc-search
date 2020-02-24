<template>
  <v-btn :type="type" color="primary">{{ title }}</v-btn>
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

<style></style>
