<template>
  <div>
    <h1>Welcome to Corporation Search.</h1>
    <h4 class="mt-3 body-1 mb-10">
      Search for active and historical BC companies by Name, Incorporation
      Number or Address.
    </h4>
    <div class="pa-10 pb-4 mb-10 corp-search-container">
      <CorporationSearch></CorporationSearch>
    </div>
    <div v-if="!isQueryEmpty">
      <div class="d-flex justify-space-between align-center mb-5">
        <h4 class="headline">Search Results</h4>
        <v-btn class="export-btn" height="50" @click="handleExport"
          >Export to .xlsx</v-btn
        >
      </div>
      <CorporationTable :corporations="corporations"></CorporationTable>
    </div>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";
import { corporationSearch, EXPORT_CORPORATION_URL } from "@/api/SearchApi.js";
import isEmpty from "lodash-es/isEmpty";
import { BACKEND_URL } from "@/config/index.ts";
const qs = require("qs");

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
      this.$root.$emit("setCorpSearchInput", nq.query);
      this.search(nq);
    }
  },
  data() {
    return {
      corporations: []
    };
  },
  methods: {
    handleExport() {
      window.open(
        `${
          process.env.VUE_APP_BACKEND_HOST
        }${EXPORT_CORPORATION_URL}/?${qs.stringify(this.$route.query)}`
      );
    },
    search(query) {
      corporationSearch(query)
        .then(result => {
          this.corporations = result.data.results;
        })
        .catch(e => {
          this.corporations = [];
        });
    }
  },
  mounted() {
    if (!this.isQueryEmpty && this.$route.query.query) {
      const query = this.$route.query.query;
      this.$root.$emit("setCorpSearchInput", query);
      this.search({
        query
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
