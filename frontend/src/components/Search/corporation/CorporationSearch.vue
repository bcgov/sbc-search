<template>
  <div class="d-flex align-top">
    <SearchInput class="d-inline-block"></SearchInput>
    <v-btn
      class="d-inline-block corporation-btn font-weight-regular ml-2"
      color="primary"
      height="55.5"
      >Search</v-btn
    >
    <v-btn
      class="d-inline-block corporation-btn font-weight-regular ml-2"
      height="55.5"
      >Clear</v-btn
    >
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corporation/SearchInput.vue";
export default {
  components: {
    SearchInput
  }
};
</script>

<style lang="scss">
.corporation-btn {
  padding: 0 2.3em !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}
</style>
