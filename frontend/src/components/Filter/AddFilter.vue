<template>
  <div class="d-flex">
    <div class="mr-2">
      <v-select
        :items="one"
        placeholder="Any Name"
        filled
        dense
        height="59"
        class="filter-input"
      ></v-select>
    </div>
    <div class="mr-2">
      <v-select
        :items="two"
        placeholder="Contains"
        filled
        dense
        height="59"
        class="filter-input"
      ></v-select>
    </div>
    <div class="mr-2">
      <v-text-field
        filled
        dense
        height="59"
        placeholder="Text..."
        class="filter-input"
      ></v-text-field>
    </div>
    <div>
      <SbcButton class="mr-2" title="Add Filter" :variant="2"></SbcButton>
      <SbcButton title="Clear" :variant="2"></SbcButton>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
export default {
  components: {
    SbcButton
  },

  data() {
    return {
      one: ["Any Name", "First Name", "Middle Name", "Last Name", "Address"],
      two: ["Contains", "Starts With", "Ends With", "Exact Match"]
    };
  }
};
</script>

<style lang="sass">
.filter-input
    width: $FILTER_INPUT_WIDTH
</style>
