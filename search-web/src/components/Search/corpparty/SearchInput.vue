<template>
  <v-text-field
    background-color="#e5e8ec"
    class="search-input"
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    :placeholder="getPlaceHolder()"
    :class="{
      'corp-search-input-md': $vuetify.breakpoint.mdOnly
    }"
    filled
    :rules="rules"
  >
    <template v-slot:append>
      <v-icon>search</v-icon>
    </template>
  </v-text-field>
</template>

<script>
import { mapGetters } from 'vuex'
export default {
  props: {
    query: {
      default: '',
      type: String
    },
    height: {
      default: 40.8,
      type: Number
    },
    uid: {
      default: null,
      type: String
    }
  },
  computed: {
    selectField () {
      return this.getFilterProperty(this.uid, 'field')
    },
    selectOperator () {
      return this.getFilterProperty(this.uid, 'operator')
    },
    ...mapGetters({
      getFilterProperty: 'corpParty/filters/getProperty'
    }),
    rules () {
      const rules = []
      if (this.selectField === 'postalCd') {
        const sixCharacters = v =>
          v.length === 6 || 'Postal Code must exactly be 6 characters'
        rules.push(sixCharacters)
      } else if (this.selectField === 'addrLine1') {
        const startsWith = v =>
          !!v.match(/\d+\s[0-9]*[a-zA-Z]+/) ||
          'Required Format: ALPHANUMERICS SPACE ALPHANUMERICS, eg. 123 Sesame'
        rules.push(startsWith)
      } else if (this.selectOperator === 'exact') {
        const notEmpty = v => !!v || 'Input cannot be empty'
        rules.push(notEmpty)
      } else {
        const atLeastThreeChar = v =>
          v.length >= 3 ||
          'Input cannot be empty and must be at least 3 characters'
        rules.push(atLeastThreeChar)
      }

      return rules
    }
  },
  data () {
    return {
      placeholder: 'Enter term here...',
      searchQuery: this.query
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.searchQuery = this.query
    })
  },
  beforeUpdate () {
    this.searchQuery = this.query
  },
  methods: {
    clear () {
      this.searchQuery = ''
    },
    getPlaceHolder () {
      switch (this.selectField) {
        case 'anyNme':
          return 'James'

        case 'firstNme':
          return 'John'

        case 'lastNme':
          return 'Smith'

        case 'middleNme':
          return 'Allan'

        case 'addrLine1':
          return '45 Sesame'

        case 'postalCd':
          return 'A1A1A1'
      }
    }
  },
  watch: {
    searchQuery (nq) {
      this.$emit('change', nq)
    }
  }
}
</script>

<style lang="scss"></style>
