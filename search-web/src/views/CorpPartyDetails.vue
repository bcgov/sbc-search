<template>
  <div>
    <h1>Director Search - Details</h1>
    <h4 class="mt-3 body-1 mb-10">
      Details for an office held at a BC Company during a specific period of
      time.
    </h4>
    <section class="detail-section">
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
  data() {
    return {
      detail: {},
      officesheld: {}
    };
  },

  mounted() {
    const corp_party_id = this.$route.params["id"];
    if (corp_party_id) {
      corpPartySearchDetail(corp_party_id).then(result => {
        this.detail = result.data;
      });
      corpPartyOfficeSearch(corp_party_id)
        .then(result => {
          this.officesheld = result.data;
        })
        .catch(() => {
          this.officesheld = {};
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
