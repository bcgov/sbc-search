<template>
  <div class="d-flex align-top">
    <SearchSelect
      class="d-inline-block mr-3"
      selectLabel="Field"
      :items="FIELDS"
      :initValue="initField"
      :uid="uid"
      property="field"
    ></SearchSelect>
    <SearchSelect
      selectLabel="Operator"
      class="d-inline-block mr-3"
      :items="operatorItems"
      :initValue="initOperator"
      :uid="uid"
      property="operator"
    ></SearchSelect>
    <SearchInput
      :uid="uid"
      :query="initQuery"
      class="d-inline-block"
    ></SearchInput>
    <v-btn tabindex="-1" v-if="remove" class="ml-5" height="56" outlined @click="handleRemove"
      >Remove</v-btn
    >
  </div>
</template>

<script>
import SearchSelect from "@/components/Search/corpparty/SearchSelect.vue";
import SearchInput from "@/components/Search/corpparty/SearchInput.vue";
import { FIELD_VALUES, OPERATOR_VALUES } from "@/config/index.ts";
import { mapGetters } from "vuex";
import filter from "lodash-es/filter";

export default {
  props: {
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
    initField: {
      default: "first_nme",
      type: String
    },
    initOperator: {
      default: "exact",
      type: String
    },
    initQuery: {
      default: "",
      type: String
    }
  },
  computed: {
    operatorItems() {
      if (this.selectedField === "addr_line_1") {
        return filter(this.OPERATORS, i => i.value === "contains");
      }
      return this.OPERATORS;
    },
    selectedField() {
      return this.getFilterProperty(this.uid, "field");
    },
    ...mapGetters({
      getFilterProperty: "corpParty/filters/getProperty"
    })
  },
  components: {
    SearchInput,
    SearchSelect
  },
  data() {
    return {
      FIELDS: FIELD_VALUES,
      OPERATORS: OPERATOR_VALUES
    };
  },
  methods: {
    handleRemove() {
      this.$store.commit("corpParty/filters/removeFilter", this.uid);
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

<style></style>
