<template>
  <div>
    <v-select :label="selectLabel" :height="height" v-model="select" :items="items"></v-select>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      default: null,
      type: Array
    },
    label: {
      default: null,
      type: String
    },
    initValue: {
      default: null,
      type: String
    },
    height: {
      default: 40,
      type: Number
    },
    selectLabel: {
      default: "Standard",
      type: String
    },
    uid: {
      default: null,
      type: Number
    },
    type: {
      default: "field",
      type: String
    }
  },
  data() {
    return {
      select: this.initValue
    };
  }
};
</script>

<style></style>
