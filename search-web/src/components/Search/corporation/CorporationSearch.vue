<template>
  <div>
    <v-form class="d-flex flex-wrap align-top">
      <div
        :class="{
          'mr-2': $vuetify.breakpoint.sm,
          'mr-3': $vuetify.breakpoint.mdAndUp,
          'w-100': $vuetify.breakpoint.xsOnly
        }"
      >
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
        <SearchInput :query.sync="searchQuery"></SearchInput>
      </div>
      <div class="break" v-if="$vuetify.breakpoint.smAndDown"></div>
      <v-btn
        class="corporation-btn font-weight-bold elevation-0 font-16"
        :class="{
          'ml-0': $vuetify.breakpoint.smAndDown,
          'ml-3': $vuetify.breakpoint.mdAndUp
        }"
        color="primary"
        height="56"
        :loading="disabled"
        :disabled="disabled"
        type="submit"
        :block="$vuetify.breakpoint.xsOnly"
        @click.prevent="handleSearch"
        >Search</v-btn
      >
      <v-btn
        v-if="disabled"
        color="warning outline font-16 font-weight-bold d-inline-block"
        height="56"
        class="sbc-button cpr-cancel-button"
        :elevation="0"
        :block="$vuetify.breakpoint.xsOnly"
        @click="abortRequest"
        :class="{
          'ml-0': $vuetify.breakpoint.xsOnly,
          'mt-3': $vuetify.breakpoint.xsOnly,
          'ml-3': $vuetify.breakpoint.smAndUp
        }"
      >
        Cancel
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import SearchInput from '@/components/Search/corporation/SearchInput.vue'
import OperatorSelect from '@/components/Search/corporation/OperatorSelect.vue'
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
    handleSearch () {
      this.$emit('search', this.searchQuery)
    },
    abortRequest () {
      this.$emit('abort')
    }
  },
  data () {
    return {
      searchQuery: null
    }
  }
}
</script>

<style lang="scss">
.corporation-btn {
  padding: 0 2.3em !important;
  letter-spacing: 0 !important;
  text-transform: none !important;
}

.break {
  flex-basis: 100%;
  height: 0;
}
</style>
