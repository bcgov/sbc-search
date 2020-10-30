<template>
  <div class="print-button-container">
    <v-icon color="#2076d2" large class="cursor-pointer" @click="handlePrint"
      >print</v-icon
    >
  </div>
</template>

<script>
export default {
  methods: {
    handlePrint () {
      window && window.print()
    }
  }
}
</script>

<style lang="scss">
@media only print {
  .print-button-container {
    display: none;
  }
}
</style>
