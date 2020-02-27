<template>
  <div>
    <h1>Corporation Details</h1>
    <h4 class="mt-3 body-1 mb-10">Details for a BC Corporation.</h4>
    <section class="detail-section" v-if="details">
      <v-row justify="space-between">
        <v-col cols="6">
          <ul class="pa-0 ma-0">
            <li
              v-for="(val, key) in filteredDetail"
              :key="key"
              class="d-flex w-100 detail-list-item"
            >
              <span
                class="font-weight-bold mb-1 detail-key"
                :class="{
                  'detail-big-margins': key === 'cessation_dt' || key === 'addr'
                }"
              >{{ getText(key) }}</span>
              <span class="detail-value">{{ val }}</span>
            </li>
          </ul>
        </v-col>
        <v-col cols="6">
          <OfficeTable :details="filteredDetail" :officesheld="officesheld"></OfficeTable>
        </v-col>
      </v-row>
      <CompanyDetails :details="details"></CompanyDetails>
    </section>
  </div>
</template>

<script>
import { companySearch } from "@/api/SearchApi.js";
import CompanyDetails from "@/components/Details/CompanyDetails.vue";
export default {
  components: {
    CompanyDetails
  },
  mounted() {
    const corporation_id = this.$route.params.id;
    if (corporation_id || corporation_id === 0) {
      companySearch(corporation_id)
        .then(result => {
          this.details = result.data;
        })
        .catch(e => {
          console.error(e);
        });
    }
  },
  data() {
    return {
      details: null
    };
  }
};
</script>

<style lang="scss">
.detail-section {
  padding: 2em 4em;
  background-color: white;
}
</style>