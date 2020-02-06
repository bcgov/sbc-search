<template>
  <div
    class="d-flex align-center toggle-container"
    @click="$emit('update:active', !active)"
  >
    <div class="toggle-title">{{ title }}</div>
    <v-icon v-if="active" color="#2a7cd4">{{ chevronUp }}</v-icon>
    <v-icon v-else color="#2a7cd4">{{ chevronDown }}</v-icon>
  </div>
</template>

<script>
import { mdiChevronUp, mdiChevronDown } from "@mdi/js";
export default {
  props: {
    title: {
      default: "Toggle",
      type: String
    },
    active: {
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      chevronUp: mdiChevronUp,
      chevronDown: mdiChevronDown
    };
  }
};
</script>

<style lang="sass">
.toggle-container
    cursor: pointer
.toggle-title
    text-decoration: underline
    color: #2a7cd4
</style>
