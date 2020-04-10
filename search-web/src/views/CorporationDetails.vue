<template>
  <div>
    <h1>Corporation Details</h1>
    <h4 class="mt-3 body-1 mb-10">Details for a BC Corporation.</h4>
    <div v-if="isLoading">
      <v-skeleton-loader
        ref="skeleton"
        :boilerplate="false"
        :type="'list-item-three-line, list-item-three-line'"
        :tile="false"
        class="mx-auto"
      ></v-skeleton-loader>
    </div>
    <div v-else-if="error">
      <v-alert
        v-model="error"
        text
        dense
        type="error"
        icon="error"
        class="mt-5 pl-6"
        border="left"
      >
        {{ errorMessage }}
      </v-alert>
    </div>
    <section v-else class="detail-section">
      <CorporationDetails :details="details"></CorporationDetails>
    </section>
  </div>
</template>

<script>
import { corporationDetailSearch } from "@/api/SearchApi.js";
import CorporationDetails from "@/components/Details/CorporationDetails.vue";
export default {
  components: {
    CorporationDetails
  },
  computed: {
    isLoading() {
      return this.details === null;
    }
  },
  mounted() {
    const corporation_id = this.$route.params.id;
    if (corporation_id || corporation_id === 0) {
      corporationDetailSearch(corporation_id)
        .then(result => {
          this.error = false;
          this.errorMessage = null;
          this.details = result.data;
        })
        .catch(error => {
          this.error = true;
          this.errorMessage = `${error.toString()} ${(error.response &&
            error.response.data.message) ||
            ""}`;
          this.details = {};
        });
    } else {
      this.error = true;
      this.errorMessage = "Corporation ID is not provided";
    }
  },
  data() {
    return {
      details: null,
      error: false,
      errorMessage: null
    };
  }
};
</script>

<style lang="scss">
.detail-section {
  padding: 2em 4em;
  background-color: white;
}

@media (max-width: 959px) {
  .detail-section {
    padding: 1em;
  }
}
</style>
