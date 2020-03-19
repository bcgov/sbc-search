<template>
  <div class="d-flex align-top">
    <FieldSelect
      class="field-select mr-3"
      :items="FIELDS"
      :init="criteria.field"
      @change="handleFieldChange"
      :selected.sync="selectedField"
    ></FieldSelect>
    <OperatorSelect
      class="field-select mr-3"
      :items="OPERATORS"
      :init="criteria.operator"
      @change="handleOperatorChange"
      :selected.sync="selectedOperator"
    ></OperatorSelect>
    <SearchInput :uid="uid" :query="initQuery" class="d-inline-block">
    </SearchInput>
    <v-btn
      tabindex="-1"
      v-if="remove"
      class="ml-5"
      height="56"
      outlined
      @click="handleRemove"
    >
      Remove
    </v-btn>
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corpparty/SearchInput.vue";
import FieldSelect from "@/components/Search/corpparty/FieldSelect.vue";
import OperatorSelect from "@/components/Search/corpparty/OperatorSelect.vue";
import { FIELD_VALUES, OPERATOR_VALUES } from "@/config/index.ts";
import { mapGetters } from "vuex";
import filter from "lodash-es/filter";

export default {
  props: {
    criteria: {
      default: null,
      type: Object
    },
    clear: {
      default: true,
      type: Boolean
    },
    remove: {
      default: false,
      type: Boolean
    },
    uid: {
      default: null,
      type: Number
    },
    initQuery: {
      default: "",
      type: String
    }
  },
  computed: {
    FIELDS() {
      return FIELD_VALUES;
    },
    OPERATORS() {
      if (this.selectedField === "addr_line_1") {
        return OPERATOR_VALUES.filter(o => o.value === "contains");
      }
      return OPERATOR_VALUES;
    }
  },
  components: {
    SearchInput,
    FieldSelect,
    OperatorSelect
  },
  data() {
    return {
      selectedField: this.criteria.field,
      selectedOperator: this.criteria.operator
    };
  },
  methods: {
    handleRemove() {
      this.$store.commit("corpParty/filters/removeFilter", this.uid);
    },
    handleFieldChange(field) {
      this.$store.commit("corpParty/filters/setSearchPropValue", {
        uid: this.uid,
        property: "field",
        value: field
      });
    },
    handleOperatorChange(operator) {
      this.$store.commit("corpParty/filters/setSearchPropValue", {
        uid: this.uid,
        property: "operator",
        value: operator
      });
    }
  },
  watch: {
    selectedField(nf) {
      if (nf === "addr_line_1") {
        this.$store.commit("corpParty/filters/setSearchPropValue", {
          uid: this.uid,
          property: "operator",
          value: "contains"
        });
      }
    }
  }
};
</script>

<style lang="scss">
.field-select {
  width: 200px;
}
</style>
