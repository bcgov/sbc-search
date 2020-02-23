<template>
  <div>
    <v-select :items="items" label="Standard"></v-select>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      default: null,
      type: Array
    }
  }
};
</script>

<style></style>
