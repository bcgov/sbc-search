<template>
  <div>
    <h1>Welcome to Corporation Search.</h1>
    <h4 class="mt-3 body-1 mb-10">Search for active and historical BC companies.</h4>
    <div class="pa-10 pb-4 mb-10 corp-search-container">
      <CorporationSearch></CorporationSearch>
    </div>
    <div class="d-flex justify-end mb-5">
      <v-btn class="export-btn" height="50">Export to .xlsx</v-btn>
    </div>
    <CorporationTable :corporations="corporations"></CorporationTable>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";

export default {
  components: {
    CorporationSearch,
    CorporationTable
  },
  data() {
    return {
      corporations: [
        {
          inc: 32131231,
          corp_nme: "The King",
          inc_date: "2019-30-31",
          addr: "#123 Sesame Street Vanocuver"
        },
        {
          inc: 32131231,
          corp_nme: "The King",
          inc_date: "2019-30-31",
          addr: "#123 Sesame Street Vanocuver"
        }
      ]
    };
  }
};
</script>

<style lang="scss">
.corp-search-container {
  background-color: white;
}
</style>
