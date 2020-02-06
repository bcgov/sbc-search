<template>
  <v-form class="d-flex">
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
        @click.native.prevent="handleClick"
        type="submit"
      ></SbcButton>
      <SbcButton
        title="Clear"
        @click.native.prevent="handleClear"
        :variant="2"
      ></SbcButton>
    </div>
  </v-form>
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
    handleClear() {
      this.field = "Any Name";
      this.operator = "Contains";
      this.value = "";
    },
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
