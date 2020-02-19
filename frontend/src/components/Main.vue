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
      <h2 class="headline text-center mb-10">
        Search for a CorpParty affilated with a company
      </h2>
      <section class="sbc-search-section">
        <Search :disabled="advancedSearchActive" />
        <SearchToggle
          title="Advanced Search"
          :active.sync="advancedSearchActive"
          class="mb-3"
        ></SearchToggle>
        <AdvancedSearch v-if="advancedSearchActive"></AdvancedSearch>
      </section>
    </section>
    <section class="sbc-results-section bg-lavender">
      <h3 class="text-center">Search Results</h3>
      <ServerSideResults class="mt-5"></ServerSideResults>
    </section>
  </div>
</template>

<script>
import Search from "@/components/Search/Search.vue";
import SearchToggle from "@/components/Search/Toggle.vue";
import AdvancedSearch from "@/components/Search/AdvancedSearch.vue";
import ServerSideResults from "@/components/Search/ServerSideTable.vue";

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
    if (this.filters.length > 0) {
      this.advancedSearchActive = true;
    }
  },
  data() {
    return {
      advancedSearchActive: false
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
