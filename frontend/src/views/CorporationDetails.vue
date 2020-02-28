<template>
  <div>
    <h1>Corporation Details</h1>
    <h4 class="mt-3 body-1 mb-10">Details for a BC Corporation.</h4>
    <section class="detail-section" v-if="details">
      <CorporationDetails :details="details"></CorporationDetails>
    </section>
  </div>
</template>

<script>
import { corporationSearch } from "@/api/SearchApi.js";
import CorporationDetails from "@/components/Details/CorporationDetails.vue";
export default {
  components: {
    CorporationDetails
  },
  mounted() {
    const corporation_id = this.$route.params.id;
    if (corporation_id || corporation_id === 0) {
      corporationSearch(corporation_id)
        .then(result => {
          this.details = result.data;
        })
        .catch(e => {});
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
