<template>
  <div class="home">
    <h1
      class="home-title font-weight-bold"
      :class="{
        'display-1': $vuetify.breakpoint.smAndDown
      }"
      @click="handleTitleClick"
    >
      {{ title }}
    </h1>
    <h4
      class="body-1 home-subtitle"
      :class="{
        'mt-4': $vuetify.breakpoint.smAndDown,
        'mb-4': $vuetify.breakpoint.smAndDown,
        'mt-3': $vuetify.breakpoint.mdAndUp,
        'mb-10': $vuetify.breakpoint.mdAndUp
      }"
    >
      Search for offices held at active and historical BC companies.
    </h4>

    <div
      class="search-form-container"
      :class="{
        'pa-5': $vuetify.breakpoint.smAndDown,
        'pa-10': $vuetify.breakpoint.mdAndUp
      }"
    >
      <SearchTips></SearchTips>
      <v-form ref="corpPartySearchForm">
        <div v-for="criteria in filters" :key="criteria.uid">
          <CorpPartySearch
            :criteria="criteria"
            :uid="criteria.uid"
            :remove="enableRemove"
          ></CorpPartySearch>
        </div>
        <AddFilterButton
          title="Add Filter"
          @click.native.prevent="addFilter"
        ></AddFilterButton>
        <div class="mt-6">
          <SearchLogic
            class="d-inline-block mr-3"
            v-if="filters.length > 1"
            :logic.sync="logic"
            :init="initLogic"
          ></SearchLogic>
          <SbcButton
            class="d-inline-block font-weight-bold"
            type="submit"
            title="Search"
            @click.native.prevent="handleNewSearch"
            :disabled="disableSearch"
          ></SbcButton>
          <v-btn
            v-if="disableSearch"
            color="warning outline font-16 font-weight-bold"
            height="56"
            class="sbc-button"
            :class="{
              'ml-0': $vuetify.breakpoint.xsOnly,
              'mt-3': $vuetify.breakpoint.xsOnly,
              'ml-3': $vuetify.breakpoint.smAndUp
            }"
            :elevation="0"
            @click="abortRequest"
            :block="$vuetify.breakpoint.xsOnly"
          >
            Cancel
          </v-btn>
        </div>
      </v-form>
      <v-alert
        v-model="error"
        dense
        type="error"
        icon="error"
        class="mt-5 pl-6"
        border="left"
      >
        {{ errorMessage }}
      </v-alert>
      <v-alert
        v-if="!error && !overload"
        v-model="warning"
        dense
        type="warning"
        icon="warning"
        class="mt-5 pl-6"
        border="left"
      >
        {{ warningMessage }}
      </v-alert>
      <v-alert
        v-if="!error || !warning"
        v-model="overload"
        dense
        type="warning"
        icon="warning"
        class="mt-5 pl-6"
        border="left"
      >
        {{ overloadMessage }}
      </v-alert>
    </div>
    <div class="mt-10">
      <div v-if="qs" class="mb-5">
        <h4 class="headline">Search Results</h4>
      </div>
      <div
        v-if="qs"
        class="sr-meta-container d-flex"
        :class="{
          'flex-column': $vuetify.breakpoint.smAndDown,
          'justify-space-between': $vuetify.breakpoint.mdAndUp,
          'align-center': $vuetify.breakpoint.mdAndUp
        }"
      >
        <SearchColumn
          @click="handleColumnClick"
          :class="{
            'mb-10': $vuetify.breakpoint.mdAndUp
          }"
          :initColumn="additionalCols"
        ></SearchColumn>

        <v-btn
          class="export-btn body-1 color-dark-grey border-gray font-16"
          :class="{
            'mb-10': $vuetify.breakpoint.smAndDown
          }"
          max-width="200"
          height="50"
          outlined
          @click="handleExport"
          :elevation="0"
          :loading="exportLoading"
          >Export to .xlsx</v-btn
        >
      </div>
      <CorpPartyTable
        @error="handleError"
        @success="handleSuccess"
        @overload="handleOverload"
        ref="corpPartyTable"
        :page="page"
        @pageUpdate="handlePageUpdate"
        @sortUpdate="handleSortUpdate"
        :qs="qs"
        :type="additionalCols"
      ></CorpPartyTable>
    </div>
  </div>
</template>

<script>
import SbcButton from '@/components/SbcButton.vue'
import SearchColumn from '@/components/Search/corpparty/SearchColumns.vue'
import AddFilterButton from '@/components/Filter/AddFilterButton.vue'
import CorpPartySearch from '@/components/Search/corpparty/CorpPartySearch.vue'
import { mapGetters } from 'vuex'
import { downloadFile, buildQueryString } from '@/util/index.ts'
import omit from 'lodash-es/omit'
import isEmpty from 'lodash-es/isEmpty'

import { exportCorpPartySearch } from '@/api/SearchApi'
import CorpPartyTable from '@/components/Search/corpparty/CorpPartyTable.vue'

import SearchLogic from '@/components/Search/corpparty/SearchLogic.vue'
import SearchTips from '@/components/Search/corpparty/SearchTips.vue'
import dayjs from 'dayjs'
const qs = require('qs')
const uniqid = require('uniqid')
export default {
  components: {
    SbcButton,
    CorpPartySearch,
    AddFilterButton,
    CorpPartyTable,
    SearchLogic,
    SearchTips,
    SearchColumn
  },
  computed: {
    enableRemove () {
      return !(this.filters && this.filters.length === 1)
    },
    ...mapGetters({
      filters: 'corpParty/filters/getFilters',
      numFilters: 'corpParty/filters/getNumFilters'
    })
  },
  data () {
    return {
      title: 'Welcome to Director Search',
      searchQuery: null,
      logic: 'ALL',
      initLogic: 'ALL',
      qs: null,
      additionalCols: 'none',
      page: '1',
      sortValue: 'lastNme',
      sortType: 'dsc',
      error: false,
      errorMessage: null,
      disableSearch: false,
      exportLoading: false,
      warning: false,
      warningMessage: null,
      overload: false,
      overloadMessage: null
    }
  },
  mounted () {
    this.resetError()
    this.resetWarning()
    this.resetOverload()
    this.init()
  },
  watch: {
    '$route.query' () {
      this.init()
    }
  },
  methods: {
    abortRequest () {
      this.$refs.corpPartyTable.cancelRequest()
    },
    handleTitleClick () {
      this.$router
        .push({
          path: '/'
        })
        .catch(e => {})
    },
    handleOverload () {
      this.overload = true
      this.overloadMessage =
        // eslint-disable-next-line max-len
        'Your search returned 165 or more results, which is the limit of the Director Search. Results will be missing at random, irrespective of sorting. Please be sure to narrow your search in order to receive a usable results list.'
    },
    resetError () {
      this.error = false
      this.errorMessage = ''
    },
    resetOverload () {
      this.overload = false
      this.overloadMessage = null
    },
    resetWarning () {
      this.warning = false
      this.warningMessage = ''
    },
    handleError (error) {
      this.disableSearch = false
      this.errorMessage = `${error.toString()} ${(error.response &&
        error.response.data.message) ||
        ''}`
      this.error = true
    },
    handleSuccess () {
      this.disableSearch = false
      this.error = false
    },
    handleExport () {
      this.exportLoading = true
      const queryString = this.generateQueryString()
      const datetime = dayjs().format('YYYY-MM-DD HH:mm:ss')
      exportCorpPartySearch(queryString)
        .then(result => {
          downloadFile(result.data, `Director Search Results ${datetime}.xlsx`)
        })
        .catch(error => {
          this.$root.$emit('openSnack', {
            text: `${error.toString()} ${(error.response &&
              error.response.data.message) ||
              ''}`,
            btnColor: 'white',
            timeout: 2000
          })
        })
        .finally(() => {
          this.exportLoading = false
        })
    },
    handlePageUpdate (page) {
      this.page = page
      this.handleSearch()
    },
    handleColumnClick (type) {
      const query = Object.assign({}, this.$route.query)
      query.additionalCols = type
      this.additionalCols = type
      this.$router
        .push({
          query
        })
        .catch(e => {
          if (e && e.name && e.name !== 'NavigationDuplicated') {
            console.error(e)
          }
        })
    },
    handleSortUpdate (options) {
      if (options.sortBy.length === 0 && options.sortDesc.length === 0) {
        this.sortValue = 'lastNme'
        this.sortType = 'dsc'
      } else {
        this.sortValue = options.sortBy[0]
        if (options.sortDesc.length > 0) {
          this.sortType = options.sortDesc[0] ? 'dsc' : 'asc'
        } else {
          this.sortType = 'dsc'
        }
      }
      this.handleSearch()
    },
    addFilter (event, field = 'firstNme', operator = 'contains', value = '') {
      this.$store.commit('corpParty/filters/addFilter', {
        uid: uniqid(),
        field,
        operator,
        value
      })
    },
    isFormValid () {
      return this.$refs.corpPartySearchForm.validate()
    },
    validateFilters () {
      const length = this.filters.length

      if (length > 1) {
        if (this.filters.find(f => f.field === 'addrLine1')) {
          return {
            warning: 'true',
            warningMessage:
              'This search may return many results and be very slow. Add more filters to improve performance'
          }
        }
      }

      // Standalone filters
      if (length === 1) {
        const field = this.filters[0].field
        const operator = this.filters[0].operator

        if (field === 'partyTypCd') {
          return {
            error: true,
            errorMessage: 'Cannot perform search by Relationship Only'
          }
        }

        if (field === 'stateTypCd') {
          return {
            error: true,
            errorMessage: 'Cannot perform search by Company Status Only'
          }
        }

        if (field === 'addrLine1') {
          return {
            error: true,
            errorMessage: 'Cannot perform search by address Only'
          }
        }

        if (field === 'postalCd') {
          return {
            warning: 'true',
            warningMessage:
              'This search may return many results and be very slow. Add more filters to improve performance'
          }
        }

        if (
          field.includes('Nme') &&
          (operator === 'nicknames' || operator === 'similar')
        ) {
          return {
            warning: 'true',
            warningMessage:
              'This search may return many results and be very slow. Add more filters to improve performance'
          }
        }

        if (
          (field === 'firstNme' || field === 'anyNme') &&
          (operator === 'contains' ||
            operator === 'startswith' ||
            operator === 'endswith')
        ) {
          return {
            warning: 'true',
            warningMessage:
              'This search may return many results and be very slow. Add more filters to improve performance'
          }
        }
      }

      return {
        warning: false,
        warningMessage: null
      }
    },
    handleNewSearch () {
      this.resetError()
      this.resetWarning()
      this.resetOverload()
      if (!this.isFormValid()) {
        return false
      }

      const result = this.validateFilters()
      if (result.error) {
        this.error = true
        this.errorMessage = result.errorMessage
        return false
      } else if (result.warning) {
        this.warning = true
        this.warningMessage = result.warningMessage
      }

      this.disableSearch = true
      this.sortValue = 'lastNme'
      this.sortType = 'dsc'
      const queryString = this.generateQueryString(1)

      this.$router
        .push({
          query: qs.parse(queryString)
        })
        .catch(e => {
          if (e && e.name && e.name === 'NavigationDuplicated') {
            this.$refs.corpPartyTable.fetchData()
          }
        })
    },
    handleSearch () {
      const queryString = this.generateQueryString()
      this.$router
        .push({
          query: qs.parse(queryString)
        })
        .catch(e => {
          if (e && e.name && e.name !== 'NavigationDuplicated') {
            console.error(e)
          }
        })
    },
    renderTable () {
      const queryString = this.generateQueryString()
      this.qs = queryString
    },
    generateQueryString (page) {
      let queryString =
        buildQueryString(this.filters) +
        `&mode=${this.logic}&additionalCols=${
          this.additionalCols
        }&page=${page || this.page}`
      if (this.sortValue && this.sortType) {
        queryString += `&sortType=${this.sortType}&sortValue=${this.sortValue}`
      }

      return queryString
    },
    init () {
      const {
        mode,
        additionalCols,
        page,
        sortValue,
        sortType
      } = this.$route.query

      if (mode) {
        this.logic = mode
        this.initLogic = mode
      }

      if (additionalCols) {
        this.additionalCols = additionalCols
      }

      if (page) {
        this.page = page
      }

      if (sortValue) {
        this.sortValue = sortValue
      }

      if (sortType) {
        this.sortType = sortType
      }

      if (isEmpty(this.$route.query)) {
        this.qs = null
      } else {
        const queryFilters = Object.assign(
          {},
          omit(
            this.$route.query,
            'mode',
            'additionalCols',
            'page',
            'sortType',
            'sortValue'
          )
        )

        if (typeof queryFilters.field === 'string') {
          queryFilters.uid = uniqid()
          this.$store.commit('corpParty/filters/setFilters', [queryFilters])
        } else if (Array.isArray(queryFilters.field)) {
          let temp = []
          const length = queryFilters.field.length
          for (let i = 0; i < length; i++) {
            temp.push({
              uid: uniqid(),
              field: queryFilters.field[i],
              operator: queryFilters.operator[i],
              value: queryFilters.value[i]
            })
          }
          this.$store.commit('corpParty/filters/setFilters', temp)
        }
        this.disableSearch = true
        this.renderTable()
      }
    }
  }
}
</script>

<style lang="scss">
.search-form-container {
  background-color: white;
}

.home-title:hover {
  text-decoration: underline;
  cursor: pointer;
}
</style>
