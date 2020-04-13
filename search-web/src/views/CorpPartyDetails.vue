<template>
  <div>
    <h1>Director Search - Details</h1>
    <h4 class="mt-3 body-1 mb-10">
      Details for an office held at a BC Company during a specific period of
      time.
    </h4>
    <div v-if="isLoading">
      <v-skeleton-loader
        ref="skeleton"
        :boilerplate="false"
        :type="'list-item-three-line, list-item-three-line, table'"
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
      <Details :detail="detail" :officesheld="officesheld"></Details>
    </section>
  </div>
</template>

<script>
import Details from "@/components/Details/Details.vue";
import {
  corpPartySearchDetail,
  corpPartyOfficeSearch
} from "@/api/SearchApi.js";
export default {
  components: {
    Details
  },
  computed: {
    isLoading() {
      return this.detail === null && this.officesheld === null;
    }
  },
  data() {
    return {
      detail: null,
      officesheld: null,
      error: false,
      errorMessage: null
    };
  },

  mounted() {
    const corp_party_id = this.$route.params["id"];
    if (corp_party_id) {
      Promise.all([
        corpPartySearchDetail(corp_party_id),
        corpPartyOfficeSearch(corp_party_id)
      ])
        .then(results => {
          this.detail = results[0].data;
          this.officesheld = results[1].data;
          this.error = false;
          this.errorMessage = null;
        })
        .catch(error => {
          this.error = true;
          this.detail = {};
          this.officesheld = {};
          this.errorMessage = `${error.toString()} ${(error.response &&
            error.response.data.message) ||
            ""}`;
        });
    }
  }
};
</script>

<style lang="scss">
.detail-section {
  padding: 2em 4em;
  background-color: white;
}
@media (max-width: 1264px) {
  .detail-section {
    padding: 1em 2em;
  }
}

@media (max-width: 599px) {
  .detail-section {
    padding: 0em 1em;
  }
}
</style>
