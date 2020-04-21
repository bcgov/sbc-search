<template>
  <div>
    <h1>Welcome to Corporation Search.</h1>
    <h4 class="mt-3 body-1 mb-10">
      Search for active and historical BC companies by Name, Incorporation
      Number or Address.
    </h4>
    <div
      class="mb-10 corp-search-container"
      :class="{
        'pa-10': $vuetify.breakpoint.smAndUp,
        'pa-2': $vuetify.breakpoint.xsOnly
      }"
    >
      <CorporationSearch
        ref="corporationSearch"
        :initOperator="initOperator"
        @search="handleSearch"
        :class="{
          'mb-n6': $vuetify.breakpoint.smAndUp
        }"
        :disabled="disableSearch"
      ></CorporationSearch>
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
        v-if="!error"
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

    <div
      v-if="!isQueryEmpty"
      class="d-flex justify-space-between align-center mb-5"
    >
      <h4 class="headline">Search Results</h4>
      <v-btn
        class="export-btn body-1 color-dark-grey border-gray font-16"
        height="50"
        @click="handleExport"
        :elevation="0"
        :loading="exportLoading"
        >Export to .xlsx</v-btn
      >
    </div>
    <CorporationTable
      ref="corporationTable"
      :page="page"
      :query="query"
      @pageUpdate="handlePageUpdate"
      @sortUpdate="handleSortUpdate"
      @error="handleError"
      @success="handleSuccess"
      @overload="handleOverload"
    ></CorporationTable>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";
import {
  corporationSearch,
  EXPORT_CORPORATION_URL,
  exportCorporationSearch
} from "@/api/SearchApi.js";
import isEmpty from "lodash-es/isEmpty";
import { downloadFile } from "@/util/index.ts";
import { BACKEND_URL } from "@/config/index.ts";
import dayjs from "dayjs";

const qs = require("qs");

export default {
  components: {
    CorporationSearch,
    CorporationTable
  },
  computed: {
    isQueryEmpty() {
      return isEmpty(this.$route.query);
    }
  },
  watch: {
    "$route.query"(nq) {
      this.$root.$emit("setCorpSearchInput", nq.query);
      this.query = nq;
    }
  },

  data() {
    return {
      error: false,
      errorMessage: null,
      overload: false,
      overloadMessage: null,
      query: null,
      page: "1",
      sort_value: "corpNme",
      sort_type: "dsc",
      disableSearch: false,
      exportLoading: false,
      initOperator: "corpNme"
    };
  },
  methods: {
    handleOverload() {
      this.overload = true;
      this.overloadMessage =
        "Your search returned 500 or more results, which is the limit of the Corporation Search. Results will be missing at random, irrespective of sorting. Please be sure to narrow your search in order to receive a usable results list.";
    },
    handleError(error) {
      this.errorMessage = `${error.toString()} ${(error.response &&
        error.response.data.message) ||
        ""}`;
      this.error = true;
      this.disableSearch = false;
    },
    resetOverload() {
      this.overload = false;
      this.overloadMessage = null;
    },
    resetError() {
      this.error = false;
      this.errorMessage = null;
    },
    handleSuccess() {
      this.error = false;
      this.disableSearch = false;
    },
    handleSearch(searchQuery) {
      this.resetError();
      this.resetOverload();
      const type = this.$refs.corporationSearch.$refs.corporationOpSelect
        .select;
      this.disableSearch = true;
      this.page = "1";
      const query = {
        query: searchQuery,
        page: 1,
        sort_type: "dsc",
        sort_value: "corpNme",
        search_field: type || "corpNme"
      };
      this.$nextTick(() => {
        this.$router
          .push({
            query
          })
          .catch(e => {
            if (e && e.name && e.name === "NavigationDuplicated") {
              this.$refs.corporationTable.fetchData(query);
            }
          });
      });
    },
    handlePageUpdate(page) {
      this.page = page;
      const query = Object.assign({}, this.$route.query);
      query.page = this.page;
      this.$router.push({ query }).catch(e => {
        if (e.name !== "NavigationDuplicated") {
          console.error(e);
        }
      });
    },
    handleSortUpdate(options) {
      if (options.sortBy.length === 0 && options.sortDesc.length === 0) {
        this.sort_type = "dsc";
        this.sort_value = "corpNme";
      } else if (options.sortBy.length === 1 && options.sortDesc.length === 1) {
        this.sort_value = options.sortBy[0];
        this.sort_type = options.sortDesc[0] ? "dsc" : "asc";
      }

      const query = Object.assign({}, this.$route.query);
      query.sort_value = this.sort_value;
      query.sort_type = this.sort_type;
      this.$router.push({ query }).catch(e => {
        if (e.name !== "NavigationDuplicated") {
          console.error(e);
        }
      });
    },
    async handleExport() {
      this.exportLoading = true;

      const queryString = qs.stringify(this.$route.query);
      const datetime = dayjs().format("YYYY-MM-DD HH:mm:ss");
      exportCorporationSearch(queryString)
        .then(result => {
          downloadFile(
            result.data,
            `Corporation Search Results ${datetime}.xlsx`
          );
        })
        .catch(error => {
          this.$root.$emit("openSnack", {
            text: `${error.toString()} ${(error.response &&
              error.response.data.message) ||
              ""}`,
            btnColor: "white",
            timeout: 2000
          });
        })
        .finally(() => {
          this.exportLoading = false;
        });
    }
  },
  mounted() {
    this.resetError();
    this.resetOverload();
    if (!this.isQueryEmpty && this.$route.query.query) {
      this.disableSearch = true;
      const query = this.$route.query;
      this.initOperator = query.search_field || "corpNme";
      this.$root.$emit("setCorpSearchInput", query.query);
      this.query = query;
      if (query.page) {
        this.page = query.page;
      }
    }
  }
};
</script>

<style lang="scss">
.corp-search-container {
  background-color: white;
}
</style>
