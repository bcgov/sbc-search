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

    <TermSelect
      v-if="selectedField === 'state_typ_cd'"
      :items="TERMS"
      :init="criteria.value || 'ACT'"
      @change="handleTermChange"
    ></TermSelect>
    <SearchInput
      v-else
      :uid="uid"
      :query="initQuery"
      class="d-inline-block"
    ></SearchInput>

    <v-btn
      tabindex="-1"
      v-if="remove"
      class="ml-5"
      height="56"
      outlined
      @click="handleRemove"
      >Remove</v-btn
    >
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corpparty/SearchInput.vue";
import FieldSelect from "@/components/Search/corpparty/FieldSelect.vue";
import OperatorSelect from "@/components/Search/corpparty/OperatorSelect.vue";
import TermSelect from "@/components/Search/corpparty/TermSelect.vue";
import { FIELD_VALUES, OPERATOR_VALUES, TERM_VALUES } from "@/config/index.ts";
import { mapGetters, mapMutations } from "vuex";
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
      } else if (this.selectedField === "state_typ_cd") {
        return OPERATOR_VALUES.filter(o => o.value === "exact");
      }
      return OPERATOR_VALUES;
    },
    TERMS() {
      return TERM_VALUES[this.selectedField];
    }
  },
  components: {
    SearchInput,
    FieldSelect,
    OperatorSelect,
    TermSelect
  },
  data() {
    return {
      selectedField: this.criteria.field,
      selectedOperator: this.criteria.operator
    };
  },
  methods: {
    ...mapMutations({
      setSearchPropValue: "corpParty/filters/setSearchPropValue"
    }),
    handleRemove() {
      this.$store.commit("corpParty/filters/removeFilter", this.uid);
    },
    handleFieldChange(field) {
      this.setSearchPropValue({
        uid: this.uid,
        property: "field",
        value: field
      });
    },
    handleOperatorChange(operator) {
      this.setSearchPropValue({
        uid: this.uid,
        property: "operator",
        value: operator
      });
    },
    handleTermChange(value) {
      this.setSearchPropValue({
        uid: this.uid,
        property: "value",
        value: value
      });
    },
    clearTerm() {
      this.$store.commit("corpParty/filters/setSearchPropValue", {
        uid: this.uid,
        property: "value",
        value: ""
      });
    }
  },
  watch: {
    selectedField(nf) {
      if (nf === "addr_line_1") {
        this.setSearchPropValue({
          uid: this.uid,
          property: "operator",
          value: "contains"
        });
        this.clearTerm();
      } else if (nf === "state_typ_cd") {
        this.setSearchPropValue({
          uid: this.uid,
          property: "operator",
          value: "exact"
        });

        const value = this.criteria.value;
        if (value !== "ACT" && value !== "HIS") {
          this.setSearchPropValue({
            uid: this.uid,
            property: "value",
            value: "ACT"
          });
        }
      } else {
        this.clearTerm();
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
