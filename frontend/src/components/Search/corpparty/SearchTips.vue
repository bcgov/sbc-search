<template>
  <div class="cursor-pointer">
    <div class="mb-4 search-tips-header" @click="open = !open">
      Search Tips
      <v-icon color="#2f7fd4" class="search-tips-icon" v-if="open">
        {{ chevronUp }}
      </v-icon>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-else>
        {{ chevronDown }}
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
        <span class="font-weight-bold">AND/OR:</span>
        AND will find results which are true for all filters only. OR will find
        results which are true for any of the filters.
      </div>
    </div>
  </div>
</template>

<script>
import { mdiChevronUp, mdiChevronDown } from "@mdi/js";
export default {
  data() {
    return {
      chevronUp: mdiChevronUp,
      chevronDown: mdiChevronDown,
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
