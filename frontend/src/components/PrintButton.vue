<template>
  <div>
    <v-icon color="#2076d2" large class="cursor-pointer" @click="handlePrint">{{
      printerIcon
    }}</v-icon>
  </div>
</template>

<script>
import { mdiPrinter } from "@mdi/js";

export default {
  data() {
    return {
      printerIcon: mdiPrinter
    };
  },
  methods: {
    handlePrint() {
      window && window.print();
    }
  }
};
</script>

<style></style>
