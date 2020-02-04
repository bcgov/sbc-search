<template>
  <div>
    <div class="d-inline-block filter-input-cell mr-2">First Name</div>
    <div class="d-inline-block filter-input-cell mr-2">Exact Match</div>
    <div class="d-inline-block filter-input-cell mr-2">Barbara</div>
    <SbcButton :variant="2" title="Remove"></SbcButton>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";

export default {
  components: {
    SbcButton
  }
};
</script>

<style lang="sass">
.filter-input-cell
    width: $FILTER_INPUT_WIDTH
    height: 50px
    padding-left: 12px
</style>
