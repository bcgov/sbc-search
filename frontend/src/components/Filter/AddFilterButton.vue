<template>
  <div>
    <v-btn color="primary">{{ title }}</v-btn>
  </div>
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

<style>
</style>