<template>
  <div>
    <section class="sbc-section">
      <h1 class="display-1 mb-6 font-weight-bold">
        Welcome To Director Search
      </h1>
      <h5 class="subtitle-1">
        Search for active and historical directorships of BC Companies
      </h5>
    </section>
    <section class="sbc-section bg-lavender pt-12">
      <section class="sbc-search-section">
        <Search :iquery="iquery" :disabled="advancedSearchActive" />
        <SearchToggle
          title="Advanced Search"
          :active.sync="advancedSearchActive"
          class="mb-3"
        ></SearchToggle>
        <AdvancedSearch
          :imode="queryMode"
          v-if="advancedSearchActive"
        ></AdvancedSearch>
      </section>
    </section>
    <section
      v-if="Object.keys($route.query).length > 0"
      class="sbc-results-section bg-lavender"
    >
      <ServerSideResults></ServerSideResults>
    </section>
  </div>
</template>

<script>
import Search from "@/components/Search/Search.vue";
import SearchToggle from "@/components/Search/Toggle.vue";
import AdvancedSearch from "@/components/Search/AdvancedSearch.vue";
import ServerSideResults from "@/components/Search/ServerSideTable.vue";
import { omit, pick } from "lodash-es";
const qs = require("qs");
import { mapState } from "vuex";
export default {
  components: {
    Search,
    SearchToggle,
    AdvancedSearch,
    ServerSideResults
  },
  computed: {
    ...mapState(["filters"])
  },
  mounted() {
    const query = this.$route.query;
    if (query.advanced) {
      const queryString = qs.parse(query.queryString);
      const queryFilters = omit(queryString, "mode");

      if (typeof queryFilters.field === "string") {
        this.queryFilters.push(queryFilters);
        this.$store.commit("addFilter", queryFilters);
        if (this.filters.length > 0) {
          this.advancedSearchActive = true;
        }
        return;
      }

      if (Array.isArray(queryFilters.field)) {
        const length = queryFilters.field.length;

        for (let i = 0; i < length; i++) {
          this.queryFilters.push({
            field: queryFilters.field[i],
            operator: queryFilters.operator[i],
            value: queryFilters.value[i]
          });
        }
      }
      this.queryMode = pick(queryString, "mode").mode;
      this.$store.commit("setFilter", this.queryFilters);
    } else if (query.query) {
      this.iquery = query.query;
    }
    if (this.filters.length > 0) {
      this.advancedSearchActive = true;
    }
  },
  data() {
    return {
      advancedSearchActive: false,
      queryFilters: [],
      queryMode: "ANY",
      iquery: null
    };
  }
};
</script>

<style lang="sass">
.sbc-search-section
  padding:  5em
  background-color: white

.sbc-results-section
  padding: 0em 5em 1em 5em
</style>
