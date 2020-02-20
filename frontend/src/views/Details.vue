<template>
  <div>
    <section class="sbc-section">
      <h1 class="display-1 mb-6 font-weight-bold">
        CorpParty Details
      </h1>
      <h5 class="font-weight-regular body-1">
        Details for an office held during a specific period of time
      </h5>
    </section>
    <section class="sbc-section bg-lavender pt-12">
      <section class="sbc-section">
        <Details></Details>
      </section>
    </section>
  </div>
</template>

<script>
import Details from "@/components/Details/Details.vue";
export default {
  components: {
    Details
  }
};
</script>

<style></style>
