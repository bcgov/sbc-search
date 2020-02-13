<template>
  <div>
    <section class="sbc-section">
      <h1 class="display-1 mb-6 font-weight-bold">
        CorpParty Search - Results
      </h1>
      <div class="body-1">Date: 19/09/03</div>
      <div class="body-1">Time: 13:51:44</div>
    </section>
    <section class="sbc-section bg-lavender pt-12">
      <h2 class="display-1 text-center mb-10">
        Search Results
      </h2>
      <div v-if="$route.query.searchQuery && !$route.query.advanced">
        <h4 class="d-inline-block mr-1">Search Term:</h4>
        <span>{{ $route.query.searchQuery }}</span>
      </div>
      <div v-if="filters.length > 0 && $route.query.advanced">
        <h4>
          Applied Filters
        </h4>
        <SearchFilter
          v-for="(filter, index) in filters"
          :key="index"
          :field="filter.field"
          :operator="filter.operator"
          :value="filter.value"
          :mode="'display'"
        ></SearchFilter>
      </div>
      <Results class="mt-10" :searchResults="searchResults"></Results>
      <ServerSideResults class="mt-5"></ServerSideResults>
    </section>
  </div>
</template>

<script>
import Results from "@/components/Search/Results.vue";
import SearchFilter from "@/components/Filter/Filter.vue";

import ServerSideResults from "@/components/Search/ServerSideTable.vue";
import { searchApi, advancedSearchApi } from "@/plugins/SearchApi.js";
import { mapState } from "vuex";

export default {
  components: {
    Results,
    ServerSideResults,
    SearchFilter
  },
  computed: {
    ...mapState(["filters"])
  },
  data() {
    return {
      searchResults: []
    };
  },
  async mounted() {
    const query = this.$route.query;

    if (!query.advanced) {
      const searchParams = {
        page: query.page,
        query: query.searchQuery
      };
      searchApi(searchParams).then(result => {
        this.searchResults = result.data.results;
      });
    } else {
      const queryString = query.queryString;
      advancedSearchApi(queryString).then(result => {
        this.searchResults = result.data.results;
      });
    }
  }
};
</script>

<style></style>
