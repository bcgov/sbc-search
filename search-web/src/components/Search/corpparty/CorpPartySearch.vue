<template>
  <div class="d-flex align-top flex-wrap cps-container">
    <FieldSelect
      class="field-select"
      :items="FIELDS"
      :init="criteria.field"
      @change="handleFieldChange"
      :selected.sync="selectedField"
      :class="{
        'mr-0': $vuetify.breakpoint.smAndDown,
        'mr-3': $vuetify.breakpoint.mdAndUp
      }"
    ></FieldSelect>
    <OperatorSelect
      class="field-select"
      :items="OPERATORS"
      :init="criteria.operator"
      @change="handleOperatorChange"
      :selected.sync="selectedOperator"
      :class="{
        'mr-0': $vuetify.breakpoint.smAndDown,
        'mr-3': $vuetify.breakpoint.mdAndUp
      }"
    ></OperatorSelect>
    <TermSelect
      v-if="selectedField === 'stateTypCd' || selectedField === 'partyTypCd'"
      :items="TERMS"
      :init="criteria.value || TERMS_INIT"
      :selected.sync="selectedTerm"
      @change="handleTermChange"
    ></TermSelect>
    <SearchInput
      ref="searchInput"
      v-else
      :uid="uid"
      :query="criteria.value"
      class="d-inline-block search-input"
      @change="handleInputChange"
    ></SearchInput>

    <v-btn
      class="text-capitalize body-1 color-dark-grey border-gray font-16"
      tabindex="-1"
      v-if="remove"
      :block="$vuetify.breakpoint.smAndDown"
      :class="{
        'ml-0': $vuetify.breakpoint.smAndDown,
        'ml-5': $vuetify.breakpoint.mdAndUp,
        'mb-10': $vuetify.breakpoint.smAndDown
      }"
      height="56"
      outlined
      @click="handleRemove"
      >Remove Filter</v-btn
    >
  </div>
</template>

<script>
import SearchInput from '@/components/Search/corpparty/SearchInput.vue'
import FieldSelect from '@/components/Search/corpparty/FieldSelect.vue'
import OperatorSelect from '@/components/Search/corpparty/OperatorSelect.vue'
import TermSelect from '@/components/Search/corpparty/TermSelect.vue'
import { FIELD_VALUES, OPERATOR_VALUES, TERM_VALUES } from '@/config/index.ts'
import { mapMutations } from 'vuex'

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
      type: String
    },
    initQuery: {
      default: '',
      type: String
    }
  },
  computed: {
    FIELDS () {
      return FIELD_VALUES
    },
    OPERATORS () {
      if (this.selectedField === 'addrLine1') {
        return OPERATOR_VALUES.filter(o => o.value === 'contains')
      } else if (this.selectedField === 'stateTypCd') {
        return OPERATOR_VALUES.filter(o => o.value === 'exact')
      } else if (this.selectedField === 'postalCd') {
        return OPERATOR_VALUES.filter(o => o.value === 'exact')
      } else if (this.selectedField === 'partyTypCd') {
        return OPERATOR_VALUES.filter(o => o.value === 'exact')
      }

      return OPERATOR_VALUES
    },
    TERMS () {
      return TERM_VALUES[this.selectedField]
    },
    TERMS_INIT () {
      if (this.selectedField === 'stateTypCd') {
        return 'ACT'
      } else if (this.selectedField === 'partyTypCd') {
        return 'DIR'
      }

      return ''
    }
  },
  components: {
    SearchInput,
    FieldSelect,
    OperatorSelect,
    TermSelect
  },
  data () {
    return {
      selectedField: this.criteria.field,
      selectedOperator: this.criteria.operator,
      selectedTerm: this.criteria.term
    }
  },
  methods: {
    ...mapMutations({
      setSearchPropValue: 'corpParty/filters/setSearchPropValue'
    }),
    handleRemove () {
      this.$store.commit('corpParty/filters/removeFilter', this.uid)
    },
    handleFieldChange (field) {
      this.setSearchPropValue({
        uid: this.uid,
        property: 'field',
        value: field
      })
      if (field === 'stateTypCd') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'exact'
        })
        const value = this.criteria.value
        if (value !== 'ACT' && value !== 'HIS') {
          this.setSearchPropValue({
            uid: this.uid,
            property: 'value',
            value: 'ACT'
          })
          this.setSearchPropValue({
            uid: this.uid,
            property: 'term',
            value: 'ACT'
          })
        }
      } else if (field === 'partyTypCd') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'exact'
        })
        const value = this.criteria.value
        if (value !== 'DIR' && value !== 'OFF' && value !== 'INC' && value !== 'ATT') {
          this.setSearchPropValue({
            uid: this.uid,
            property: 'value',
            value: 'DIR'
          })
          this.setSearchPropValue({
            uid: this.uid,
            property: 'term',
            value: 'DIR'
          })
        }
      }
    },
    handleOperatorChange (operator) {
      this.setSearchPropValue({
        uid: this.uid,
        property: 'operator',
        value: operator
      })
    },
    handleTermChange (value) {
      this.setSearchPropValue({
        uid: this.uid,
        property: 'value',
        value: value
      })
    },
    handlePartyTypeChange (value) {
      this.setSearchPropValue({
        uid: this.uid,
        property: 'value',
        value: value
      })
    },
    handleInputChange (value) {
      this.setSearchPropValue({
        uid: this.uid,
        property: 'value',
        value: value
      })
    },
    clearTerm () {
      this.$store.commit('corpParty/filters/setSearchPropValue', {
        uid: this.uid,
        property: 'value',
        value: ''
      })
    }
  },
  watch: {
    selectedField (nf, of) {
      if (nf === 'addrLine1') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'contains'
        })
      } else if (nf === 'stateTypCd') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'exact'
        })
        const value = this.criteria.value
        if (value !== 'ACT' && value !== 'HIS') {
          this.setSearchPropValue({
            uid: this.uid,
            property: 'value',
            value: 'ACT'
          })
          this.setSearchPropValue({
            uid: this.uid,
            property: 'term',
            value: 'ACT'
          })
        }
      } else if (nf === 'postalCd') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'exact'
        })
      } else if (nf === 'partyTypCd') {
        this.setSearchPropValue({
          uid: this.uid,
          property: 'operator',
          value: 'exact'
        })
        const value = this.criteria.value
        if (value !== 'DIR' && value !== 'OFF' && value !== 'INC' && value !== 'ATT') {
          this.setSearchPropValue({
            uid: this.uid,
            property: 'value',
            value: 'DIR'
          })
          this.setSearchPropValue({
            uid: this.uid,
            property: 'term',
            value: 'DIR'
          })
        }
      } else if (of === 'stateTypCd') {
        this.clearTerm()
      } else if (of === 'partyTypCd') {
        this.clearTerm()
      }
    }
  }
}
</script>

<style lang="scss">
.cps-container {
  flex-wrap: wrap;
}
.field-select {
  width: 200px;
}

@media (max-width: 1497px) {
  .search-input {
    width: 150px;
  }
}

@media (max-width: 1264px) {
  .field-select {
    width: 180px;
  }
}

@media (max-width: 959px) {
  .field-select {
    width: 100%;
  }
  .search-input {
    width: 100% !important;
  }
}

@media (max-width: 599px) {
  .field-select {
    width: 100% !important;
  }
}
</style>
