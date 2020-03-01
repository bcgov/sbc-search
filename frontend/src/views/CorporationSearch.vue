<template>
  <div>
    <h1>Welcome to Corporation Search</h1>
    <h4 class="mt-3 body-1 mb-10">
      Search for active and historical BC companies
    </h4>

    <CorporationSearch></CorporationSearch>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
export default {
  components: {
    CorporationSearch
  }
};
</script>

<style></style>
