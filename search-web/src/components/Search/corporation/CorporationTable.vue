<template>
  <div>
    <v-data-table
      v-if="query"
      class="corporation-table"
      mobile-breakpoint="960"
      :loading="loading"
      :headers="headers"
      :options.sync="options"
      :disable-sort="disableSorting"
      :items="corporations"
      @update:sort-by="updateSort"
      @update:sort-desc="updateSort"
      :sort-by="sortBy"
      :sort-desc="sortDesc"
      :footer-props="{
        'items-per-page-options': [items_per_page]
      }"
    >
      <template v-slot:top="{}">
        <div class="v-data-footer v-data-custom-header">
          <div
            v-if="corporations.length === 0"
            class="v-data-footer__pagination"
          >
            &ndash;
          </div>
          <div v-else class="v-data-footer__pagination">
            <div class="custom-footer d-flex align-center">
              <div>
                Showing {{ showingMin }}-{{ showingMax }} of
                {{ totalItems }} results
              </div>
              <div class="d-flex ml-5 align-center">
                <v-btn
                  v-if="page > '1' && !loading"
                  icon
                  @click="pagePrev"
                  small
                >
                  <v-icon>arrow_back</v-icon>
                </v-btn>
                <v-btn v-else disabled icon small>
                  <v-icon>arrow_back</v-icon>
                </v-btn>
                <div class="d-inline-block mr-3 ml-3">Page {{ page }}</div>
                <v-btn
                  icon
                  v-if="showingMax < totalItems && !loading"
                  @click="pageNext"
                  small
                >
                  <v-icon>arrow_forward</v-icon>
                </v-btn>
                <v-btn icon v-else disabled small>
                  <v-icon>arrow_forward</v-icon>
                </v-btn>
              </div>
            </div>
          </div>
        </div>
      </template>
      <template v-slot:item="{ item, index, headers }">
        <!-- Mobile View Begin -->
        <tr
          @click="handleTableRowClick(item, $event)"
          class="cursor-pointer d-table-row d-md-none mobile-tr-row"
          v-for="(value, i) in Object.values(orderItems(item))"
          :key="`row${index}${value}${i}`"
        >
          <td class="d-table-cell">
            <div class="d-flex w-100 justify-space-between">
              <div class="color-black">{{ headers[i] && headers[i].text }}</div>
              <div class="text-right">{{ value }}</div>
            </div>
          </td>
        </tr>
        <v-divider class="d-md-none" />
        <!-- Mobile View End -->

        <tr
          class="cursor-pointer d-none d-md-table-row"
          @click="handleTableRowClick(item, $event)"
        >
          <td class="anchor-text">{{ item["corpNum"] }}</td>
          <td>{{ item["corpTypCd"] }}</td>
          <td>{{ item["corpNme"] }}</td>
          <td>{{ formatDate(item["recognitionDts"]) }}</td>
          <td>{{ item["stateTypCd"] }}</td>
        </tr>
      </template>
      <template v-slot:footer>
        <v-progress-linear
          :active="loading"
          :indeterminate="true"
          color="primary"
          height="2"
        ></v-progress-linear>
      </template>
      <template v-slot:footer.page-text="{}">
        <div class="custom-footer d-flex align-center">
          <div>
            Showing {{ showingMin }}-{{ showingMax }} of
            {{ totalItems }} results
          </div>
          <div class="d-flex ml-5 align-center">
            <v-btn v-if="page > '1' && !loading" icon @click="pagePrev" small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <v-btn v-else disabled icon small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <div class="d-inline-block mr-3 ml-3">Page {{ page }}</div>
            <v-btn
              icon
              v-if="showingMax < totalItems && !loading"
              @click="pageNext"
              small
            >
              <v-icon>arrow_forward</v-icon>
            </v-btn>
            <v-btn icon v-else disabled small>
              <v-icon>arrow_forward</v-icon>
            </v-btn>
          </div>
        </div>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { CORPORATION_HEADERS } from '@/config/index.ts'
import { corporationSearch } from '@/api/SearchApi'
import axios from 'axios'
import { formatDate } from '@/util/index.ts'
import pick from 'lodash-es/pick'

export default {
  props: {
    query: {
      default: null,
      type: Object
    },
    page: {
      default: '1',
      type: String
    }
  },
  computed: {
    headers () {
      const filter = {
        addr: true,
        postalCd: true
      }
      return CORPORATION_HEADERS.filter(ch => !filter[ch.value])
    },
    showingMin () {
      if (this.page === 1) {
        return 1
      }
      let min = 0
      for (let i = 0; i < this.page - 1; i++) {
        min += this.items_per_page
      }
      return min
    },
    showingMax () {
      if (this.corporations.length < this.items_per_page && this.page === 1) {
        return this.corporations.length
      }
      if (this.corporations.length < this.items_per_page && this.page !== 1) {
        return this.showingMin + this.corporations.length
      }
      return this.page * this.items_per_page
    }
  },
  data () {
    return {
      corporations: [],
      loading: false,
      totalItems: 0,
      options: {},
      disableSorting: false,
      sortBy: [],
      sortDesc: [],
      items_per_page: 50,
      source: null
    }
  },
  methods: {
    formatDate,
    orderItems (items) {
      return pick(items, [
        'corpNum',
        'corpTypCd',
        'corpNme',
        'recognitionDts',
        'stateTypCd'
      ])
    },
    pageNext () {
      this.$emit('pageUpdate', (parseInt(this.page) + 1).toString())
    },
    pagePrev () {
      if (this.page > '1') {
        this.$emit('pageUpdate', (parseInt(this.page) - 1).toString())
      }
    },
    updateSort () {
      this.$emit('sortUpdate', {
        sortBy: this.options.sortBy,
        sortDesc: this.options.sortDesc
      })
    },
    handleTableRowClick (item, e) {
      e.target.closest('tr').classList.add('row-clicked')
      this.$router.push('/corporation/' + item['corpNum'])
    },
    cancelRequest () {
      this.source && this.source.cancel('Request aborted by user')
    },
    async fetchData (query) {
      const { sortType, sortValue } = query
      this.sortBy = [sortValue]
      if (sortType === 'asc') {
        this.sortDesc = [false]
      } else if (sortType === 'dsc') {
        this.sortDesc = [true]
      }
      this.loading = true
      this.disableSorting = true

      const CancelToken = axios.CancelToken
      this.source = CancelToken.source()

      corporationSearch(query, this.source.token)
        .then(result => {
          this.corporations = result.data.results
          this.totalItems = result.data.numResults
          this.$emit('success', result)
          // eslint-disable-next-line no-unused-expressions
          this.totalItems >= 165 ? this.$emit('overload') : ''
        })
        .catch(e => {
          this.corporations = []
          this.totalItems = 0
          this.$emit('error', e)
        })
        .finally(() => {
          this.disableSorting = false
          this.loading = false
        })
    }
  },
  watch: {
    query (nq) {
      this.fetchData(nq)
    }
  }
}
</script>
<style lang="scss">
.corporation-table .custom-footer {
  padding: 1em 0;
}

.corporation-table .v-data-footer__icons-after,
.corporation-table .v-data-footer__icons-before {
  display: none;
}

.v-data-custom-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.row-clicked {
  background-color: $COLOR_LAVENDER !important;
}
.corporation-table .v-data-table__wrapper {
  overflow-x: auto;
  background-image: linear-gradient(to right, #ffffff, rgba(255, 255, 255, 0)),
    linear-gradient(to left, #ffffff, rgba(255, 255, 255, 0)),
    linear-gradient(to right, #e0e0e0, rgba(0, 0, 0, 0)),
    linear-gradient(to left, #e0e0e0, rgba(0, 0, 0, 0));
  background-position: 0 0, 100% 0, 0 0, 100% 0;
  background-repeat: no-repeat;
  background-color: white;
  background-size: 4em 100%, 4em 100%, 2em 100%, 2em 100%;
  background-attachment: local, local, scroll, scroll;
}
</style>
