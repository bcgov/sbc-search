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
      <Results :searchResults="searchResults"></Results>
    </section>
  </div>
</template>

<script>
import Results from "@/components/Search/Results.vue";
import { searchApi, advancedSearchApi } from "@/plugins/SearchApi.js";

export default {
  components: {
    Results
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
      searchApi(searchParams)
        .then(result => {
          this.searchResults = result.data.results;
        })
        .catch(e => console.error(e));
    } else {
      const queryString = query.queryString;
      advancedSearchApi(queryString)
        .then(result => {
          this.searchResults = result.data.results;
        })
        .catch(e => console.error(e));
    }
  }
};
</script>

<style></style>
