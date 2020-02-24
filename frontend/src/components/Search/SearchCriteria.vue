<template>
  <div>
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
      :items="OPERATORS"
      :initValue="initOperator"
      :uid="uid"
      property="operator"
    ></SearchSelect>
    <SearchInput
      :uid="uid"
      :query="initQuery"
      class="d-inline-block mt-2"
    ></SearchInput>
    <v-btn v-if="remove" class="ml-5" outlined small @click="handleRemove"
      >Remove</v-btn
    >
  </div>
</template>

<script>
import SearchSelect from "@/components/Search/SearchSelect.vue";
import SearchInput from "@/components/Search/SearchInput.vue";
import { FIELD_VALUES, OPERATOR_VALUES } from "@/config/index.js";
import { mapState } from "vuex";

export default {
  props: {
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
      this.$store.commit("filters/removeFilter", this.uid);
    }
  }
};
</script>

<style></style>
