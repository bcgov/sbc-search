<template>
  <div>
    <div v-if="mode === 'filter'">
      <div class="d-inline-block filter-input-cell mr-2">
        {{ getText(field, "field") }}
      </div>
      <div class="d-inline-block filter-input-cell mr-2">
        {{ getText(operator, "operator") }}
      </div>
      <div class="d-inline-block filter-input-cell mr-2 font-weight-bold">
        {{ value }}
      </div>
      <SbcButton
        :variant="2"
        :width="120"
        title="Remove"
        @click.native="handleRemove"
      ></SbcButton>
    </div>
    <div v-else>
      <div class="d-inline-block mr-2">
        {{ getText(field, "field") }}
      </div>
      <div class="d-inline-block mr-2">
        {{ getText(operator, "operator") }}
      </div>
      <div class="d-inline-block mr-2">{{ value }}</div>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import { getTextFromValues } from "@/plugins/utils.js";
import { FIELD_VALUES, OPERATOR_VALUES } from "@/plugins/config.js";

export default {
  props: {
    field: {
      default: "N/A",
      type: String
    },
    operator: {
      default: "N/A",
      type: String
    },
    value: {
      default: "N/A",
      type: String
    },
    mode: {
      default: "filter",
      type: String
    }
  },
  components: {
    SbcButton
  },
  methods: {
    handleRemove() {
      const filter = {
        field: this.field,
        operator: this.operator,
        value: this.value
      };
      return this.$store.commit("removeFilter", filter);
    },
    getText(data, type) {
      if (type === "field") {
        return getTextFromValues(FIELD_VALUES, data);
      }
      if (type === "operator") {
        return getTextFromValues(OPERATOR_VALUES, data);
      }
    }
  }
};
</script>

<style lang="sass">
.filter-input-cell
    width: $FILTER_INPUT_WIDTH
    height: 50px
    padding-left: 12px
</style>
