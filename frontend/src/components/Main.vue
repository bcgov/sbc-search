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
      <section class="sbc-section">
        <Search :disabled="advancedSearchActive" />
        <SearchToggle
          title="Advanced Search"
          :active.sync="advancedSearchActive"
          class="mb-3"
        ></SearchToggle>
        <AdvancedSearch v-if="advancedSearchActive"></AdvancedSearch>
      </section>
    </section>
  </div>
</template>

<script>
import Search from "@/components/Search/Search.vue";
import SearchToggle from "@/components/Search/Toggle.vue";
import AdvancedSearch from "@/components/Search/AdvancedSearch.vue";
export default {
  components: {
    Search,
    SearchToggle,
    AdvancedSearch
  },
  data() {
    return {
      advancedSearchActive: false
    };
  }
};
</script>

<style lang="sass"></style>
