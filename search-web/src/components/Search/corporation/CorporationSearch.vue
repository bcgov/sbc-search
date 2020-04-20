<template>
  <div>
    <v-form class="d-flex flex-wrap align-top">
      <div class="mr-2">
        <OperatorSelect
          :initOperator="initOperator"
          ref="corporationOpSelect"
        ></OperatorSelect>
      </div>
      <div
        class="search-input-container"
        :class="{
          'w-100': $vuetify.breakpoint.xsOnly
        }"
      >
        <SearchInput
          class="d-inline-block"
          :query.sync="searchQuery"
        ></SearchInput>
      </div>
      <v-btn
        class="d-inline-block corporation-btn font-weight-bold elevation-0 font-16"
        color="primary"
        height="56"
        :disabled="disabled"
        type="submit"
        :block="$vuetify.breakpoint.xsOnly"
        @click.prevent="handleSearch"
        :class="{
          'ml-2': $vuetify.breakpoint.smAndUp,
          'ml-0': $vuetify.breakpoint.xsOnly
        }"
        >Search</v-btn
      >
    </v-form>
  </div>
</template>

<script>
import SearchInput from "@/components/Search/corporation/SearchInput.vue";
import OperatorSelect from "@/components/Search/corporation/OperatorSelect.vue";
export default {
  components: {
    SearchInput,
    OperatorSelect
  },
  props: {
    initOperator: {
      default: null,
      type: String
    },
    initSearch: {
      default: null,
      type: String
    },
    disabled: {
      default: false,
      type: Boolean
    }
  },
  methods: {
    handleSearch() {
      this.$emit("search", this.searchQuery);
    }
  },
  data() {
    return {
      searchQuery: null
    };
  }
};
</script>

<style lang="scss">
.corporation-btn {
  padding: 0 2.3em !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}
</style>
