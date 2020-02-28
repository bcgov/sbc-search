<template>
  <div>
    <v-btn class="add-filter-button sbc-button" height="50">
      <v-icon left>{{ plusIcon }}</v-icon>
      {{ title }}
    </v-btn>
  </div>
</template>

<script>
import { mdiPlus } from "@mdi/js";
export default {
  props: {
    title: {
      default: null,
      type: String
    }
  },
  data() {
    return {
      plusIcon: mdiPlus
    };
  }
};
</script>

<style lang="scss"></style>
