<template>
  <div>
    <v-form class="d-flex align-top">
      <SearchInput class="d-inline-block" :query.sync="searchQuery"></SearchInput>
      <v-btn
        class="d-inline-block corporation-btn font-weight-regular ml-2"
        color="primary"
        height="55.5"
        type="submit"
        @click.prevent="handleSearch"
      >Search</v-btn>
      <v-btn
        @click="handleClear"
        class="d-inline-block corporation-btn font-weight-regular ml-2"
        height="55.5"
      >Clear</v-btn>
    </v-form>
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corporation/SearchInput.vue";
export default {
  components: {
    SearchInput
  },
  methods: {
    handleSearch() {
      const query = this.searchQuery;
      this.$router.push({
        query: {
          query
        }
      });
    },
    handleClear() {
      this.$root.$emit("clearCorpSearchInput");
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
