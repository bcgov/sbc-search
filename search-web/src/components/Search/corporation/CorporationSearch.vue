<template>
  <div>
    <v-form class="d-flex flex-wrap align-top">
      <div
        class="search-input-container"
        :class="{
          'w-100': $vuetify.breakpoint.xsOnly
        }"
      >
        <SearchInput
          class="d-inline-block"
          :query.sync="searchQuery"
        ></SearchInput>
      </div>
      <v-btn
        class="d-inline-block corporation-btn font-weight-regular"
        color="primary"
        height="55.5"
        type="submit"
        :block="$vuetify.breakpoint.xsOnly"
        @click.prevent="handleSearch"
        :class="{
          'ml-2': $vuetify.breakpoint.smAndUp,
          'ml-0': $vuetify.breakpoint.xsOnly
        }"
        >Search</v-btn
      >
    </v-form>
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corporation/SearchInput.vue";
export default {
  components: {
    SearchInput
  },
  props: {
    initSearch: {
      default: null,
      type: String
    }
  },
  methods: {
    handleSearch() {
      this.$emit("search", this.searchQuery);
    }
  },
  data() {
    return {
      searchQuery: null
    };
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
