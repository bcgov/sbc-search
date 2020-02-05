<template>
  <div>
    <section class="sbc-section">
      <h1 class="display-1 mb-6 font-weight-bold">
        CorpParty Details
      </h1>
      <h5 class="subtitle-1">
        Lorem ipsum
      </h5>
    </section>
    <section class="sbc-section bg-lavender pt-12">
      <h2 class="headline text-center mb-10">
        CorpParty Details
      </h2>
      <section class="sbc-section">
        <v-container>
          <v-row>
            <v-col cols="6">
              <Details></Details>
            </v-col>
            <v-col cols="6">
              <OfficeTable
                title="All Offices held at Dennis Black Consulting Ltd."
              ></OfficeTable>
            </v-col>
          </v-row>
        </v-container>
      </section>
    </section>
  </div>
</template>

<script>
import Details from "@/components/Details/Details.vue";
import OfficeTable from "@/components/Details/OfficeTable.vue";
export default {
  components: {
    Details,
    OfficeTable
  }
};
</script>

<style></style>
