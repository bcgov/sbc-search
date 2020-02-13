<template>
  <v-form class="d-flex" ref="filterForm" lazy-validation v-model="valid">
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
        :rules="valueRules"
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
        type="submit"
        @click.native.prevent="handleClick"
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
      valid: true,
      field: "ANY_NME",
      operator: "contains",
      value: null,
      fields: FIELD_VALUES,
      operators: OPERATOR_VALUES,
      valueRules: [n => (n && n.length > 0) || "Text cannot be empty"]
    };
  },

  methods: {
    handleClear() {
      this.field = "ANY_NME";
      this.operator = "contains";
      this.value = "";
    },
    handleClick() {
      if (!this.$refs.filterForm.validate()) {
        return false;
      }
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
