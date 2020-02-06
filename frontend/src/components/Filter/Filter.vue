<template>
  <div>
    <div class="d-inline-block filter-input-cell mr-2">
      {{ getText(field, "field") }}
    </div>
    <div class="d-inline-block filter-input-cell mr-2">
      {{ getText(operator, "operator") }}
    </div>
    <div class="d-inline-block filter-input-cell mr-2">{{ value }}</div>
    <SbcButton :variant="2" :width="120" title="Remove"></SbcButton>
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
    }
  },
  components: {
    SbcButton
  },
  methods: {
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
