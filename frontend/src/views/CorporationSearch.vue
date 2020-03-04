<template>
  <div>
    <h1>Welcome to Corporation Search.</h1>
    <h4
      class="mt-3 body-1 mb-10"
    >Search for active and historical BC companies by Name, Incorporation Number or Address.</h4>
    <div class="pa-10 pb-4 mb-10 corp-search-container">
      <CorporationSearch :initSearch="initSearch"></CorporationSearch>
    </div>
    <div v-if="!isQueryEmpty">
      <div class="d-flex justify-space-between align-center mb-5">
        <h4 class="headline">Search Results</h4>
        <v-btn class="export-btn" height="50">Export to .xlsx</v-btn>
      </div>
      <CorporationTable :corporations="corporations"></CorporationTable>
    </div>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";
import { corporationSearch } from "@/api/SearchApi.js";
import { isEmpty } from "lodash-es";

export default {
  components: {
    CorporationSearch,
    CorporationTable
  },
  computed: {
    isQueryEmpty() {
      return isEmpty(this.$route.query);
    }
  },
  watch: {
    "$route.query"(nq) {
      this.search(nq);
    }
  },
  data() {
    return {
      corporations: [],
      initSearch: null
    };
  },
  methods: {
    search(query) {
      corporationSearch(query)
        .then(result => {
          this.corporations = result.data.results;
        })
        .catch(e => {
          this.corporations = [];
        });
    }
  }
};
</script>

<style lang="scss">
.corp-search-container {
  background-color: white;
}
</style>
