<template>
  <div class="cursor-pointer">
    <div class="mb-4" @click="open = !open">
      <div class="search-tips-header d-inline-block">Search Tips</div>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-if="open">
        keyboard_arrow_up
      </v-icon>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-else>
        keyboard_arrow_down
      </v-icon>
    </div>
    <div v-if="open">
      <div class="mb-4">
        <span class="font-weight-bold">Search By Names:</span>
        Search by first and last name below. Modify/remove/add filters as
        needed.
      </div>
      <div class="mb-4">
        <span class="font-weight-bold">Search By Street Address:</span>
        Try entering the building number and street name. Add another filter to
        enter postal code, for added accuracy.
      </div>
      <div class="mb-4">
        <span class="font-weight-bold">ALL/ANY:</span>
        ALL will find results which are true for all filters only. ANY will find
        results which are true for any of the filters.
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      open: false
    };
  }
};
</script>

<style lang="scss">
.search-tips-header {
  color: #2f7fd4;
  text-decoration: underline;
}
</style>
