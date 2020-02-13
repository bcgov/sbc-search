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
      <div v-if="$route.query.advanced">
        <h4>
          Applied Filters
        </h4>
        <SearchFilter
          v-for="(f, index) in filters"
          :key="index"
          :field="f.field"
          :operator="f.operator"
          :value="f.value"
          :mode="'display'"
        ></SearchFilter>
      </div>
      <ServerSideResults class="mt-5"></ServerSideResults>
    </section>
  </div>
</template>

<script>
import SearchFilter from "@/components/Filter/Filter.vue";
import ServerSideResults from "@/components/Search/ServerSideTable.vue";
import { mapState } from "vuex";
import { omit, pick } from "lodash-es";
const qs = require("qs");

export default {
  components: {
    ServerSideResults,
    SearchFilter
  },
  computed: {
    ...mapState(["filters"])
  },
  data() {
    return {
      searchResults: [],
      queryFilters: [],
      queryMode: null
    };
  },
  async mounted() {
    const query = this.$route.query;

    const queryString = qs.parse(query.queryString);
    this.queryFilters = omit(queryString, "mode");
    this.queryMode = pick(queryString, "mode");
  }
};
</script>

<style></style>
