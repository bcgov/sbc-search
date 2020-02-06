<template>
  <div class="d-flex">
    <div class="mr-2">
      <v-select
        v-model="field"
        :items="fields"
        placeholder="Any Name"
        filled
        dense
        height="59"
        class="filter-input"
      ></v-select>
    </div>
    <div class="mr-2">
      <v-select
        v-model="operator"
        :items="operators"
        placeholder="Contains"
        filled
        dense
        height="59"
        class="filter-input"
      ></v-select>
    </div>
    <div class="mr-2">
      <v-text-field
        v-model="value"
        filled
        dense
        height="59"
        placeholder="Text..."
        class="filter-input"
      ></v-text-field>
    </div>
    <div>
      <SbcButton
        class="mr-2"
        :width="120"
        title="Add Filter"
        :variant="2"
        @click.native="handleClick"
      ></SbcButton>
      <SbcButton title="Clear" :variant="2"></SbcButton>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import { FIELD_VALUES, OPERATOR_VALUES } from "@/plugins/config.js";

export default {
  components: {
    SbcButton
  },

  data() {
    return {
      field: null,
      operator: null,
      value: null,
      fields: FIELD_VALUES,
      operators: OPERATOR_VALUES
    };
  },

  methods: {
    handleClick() {
      const filter = {
        field: this.field,
        operator: this.operator,
        value: this.value
      };
      this.$store.commit("addFilter", filter);
    }
  }
};
</script>

<style lang="sass">
.filter-input
    width: $FILTER_INPUT_WIDTH
</style>
