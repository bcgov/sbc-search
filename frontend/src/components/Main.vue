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
        <Search />
        <AdvancedSearch></AdvancedSearch>
      </section>
    </section>
  </div>
</template>

<script>
import Search from "@/components/Search/Search.vue";
import AdvancedSearch from "@/components/Search/AdvancedSearch.vue";
export default {
  components: {
    Search,
    AdvancedSearch
  }
};
</script>

<style lang="sass"></style>
