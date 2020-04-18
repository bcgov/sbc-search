<template>
  <div class="home">
    <h1
      class="home-title font-weight-bold"
      :class="{
        'display-1': $vuetify.breakpoint.smAndDown
      }"
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
        <div v-for="criteria in filters">
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
        </div>
      </v-form>
      <v-alert
        v-model="error"
        text
        dense
        type="error"
        icon="error"
        class="mt-5 pl-6"
        border="left"
      >
        {{ errorMessage }}
      </v-alert>
      <v-alert
        v-if="warning && !error"
        v-model="warning"
        text
        dense
        type="warning"
        icon="warning"
        class="mt-5 pl-6"
        border="left"
      >
        {{ warningMessage }}
      </v-alert>
    </div>
    <div class="mt-10">
      <div v-if="qs" class="mb-5">
        <h4 class="headline">Search Results</h4>
      </div>
      <div v-if="qs" class="d-flex justify-space-between align-center">
        <SearchColumn
          @click="handleColumnClick"
          class="mb-10"
          :initColumn="additional_cols"
        ></SearchColumn>

        <v-btn
          class="export-btn body-1 color-dark-grey border-gray font-16"
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
        ref="corpPartyTable"
        :page="page"
        @pageUpdate="handlePageUpdate"
        @sortUpdate="handleSortUpdate"
        :qs="qs"
        :type="additional_cols"
      ></CorpPartyTable>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import SearchColumn from "@/components/Search/corpparty/SearchColumns.vue";
import AddFilterButton from "@/components/Filter/AddFilterButton.vue";
import CorpPartySearch from "@/components/Search/corpparty/CorpPartySearch.vue";
import { mapGetters } from "vuex";
import { downloadFile } from "@/util/index.ts";
import omit from "lodash-es/omit";
import isEmpty from "lodash-es/isEmpty";
const qs = require("qs");
import {
  searchApi,
  EXPORT_CORPPARTY_URL,
  exportCorpPartySearch
} from "@/api/SearchApi";
import CorpPartyTable from "@/components/Search/corpparty/CorpPartyTable.vue";
import { buildQueryString } from "@/util/index.ts";
import SearchLogic from "@/components/Search/corpparty/SearchLogic.vue";
import SearchTips from "@/components/Search/corpparty/SearchTips.vue";
import { BACKEND_URL } from "@/config/index.ts";
import dayjs from "dayjs";
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
    enableRemove() {
      return !(this.filters && this.filters.length === 1);
    },
    ...mapGetters({
      filters: "corpParty/filters/getFilters",
      numFilters: "corpParty/filters/getNumFilters"
    })
  },
  data() {
    return {
      title: "Welcome to Director Search",
      uid: 2,
      searchQuery: null,
      logic: "ALL",
      initLogic: "ALL",
      qs: null,
      additional_cols: "none",
      page: "1",
      sort_value: "lastNme",
      sort_type: "dsc",
      error: false,
      errorMessage: null,
      disableSearch: false,
      exportLoading: false,
      warning: false,
      warningMessage: null
    };
  },
  mounted() {
    this.init();
  },
  watch: {
    "$route.query"() {
      this.init();
    }
  },
  methods: {
    resetError() {
      this.error = false;
      this.errorMessage = "";
    },
    resetWarning() {
      this.warning = false;
      this.warningMessage = "";
    },
    handleError(error) {
      this.disableSearch = false;
      this.errorMessage = `${error.toString()} ${(error.response &&
        error.response.data.message) ||
        ""}`;
      this.error = true;
    },
    handleSuccess() {
      this.disableSearch = false;
      this.error = false;
    },
    handleExport() {
      this.exportLoading = true;
      const queryString = this.generateQueryString();
      const datetime = dayjs().format("YYYY-MM-DD HH:mm:ss");
      exportCorpPartySearch(queryString)
        .then(result => {
          downloadFile(result.data, `Director Search Results ${datetime}.xlsx`);
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
    },
    handlePageUpdate(page) {
      this.page = page;
      this.handleSearch();
    },
    handleColumnClick(type) {
      const query = Object.assign({}, this.$route.query);
      query.additional_cols = type;
      this.additional_cols = type;
      this.$router
        .push({
          query
        })
        .catch(e => {
          if (e && e.name && e.name !== "NavigationDuplicated") {
            console.error(e);
          }
        });
    },
    handleSortUpdate(options) {
      if (options.sortBy.length === 0 && options.sortDesc.length === 0) {
        this.sort_value = "lastNme";
        this.sort_type = "dsc";
      } else {
        this.sort_value = options.sortBy[0];
        if (options.sortDesc.length > 0) {
          this.sort_type = options.sortDesc[0] ? "dsc" : "asc";
        } else {
          this.sort_type = "dsc";
        }
      }
      this.handleSearch();
    },
    addFilter(event, field = "firstNme", operator = "contains", value = "") {
      this.uid++;
      this.$store.commit("corpParty/filters/addFilter", {
        uid: this.uid,
        field,
        operator,
        value
      });
    },
    isFormValid() {
      return this.$refs.corpPartySearchForm.validate();
    },
    validateFilters() {
      const length = this.filters.length;

      if (length > 1) {
        if (this.filters.find(f => f.field === "addrLine1")) {
          return {
            warning: "true",
            warningMessage:
              "This search may return many results and be very slow. Add more filters to improve performance"
          };
        }
      }

      //Standalone filters
      if (length === 1) {
        const field = this.filters[0].field;
        const operator = this.filters[0].operator;

        if (field === "stateTypCd") {
          return {
            error: true,
            errorMessage: "Cannot perform search by Company Status Only"
          };
        }

        if (field === "addrLine1")
          return {
            error: true,
            errorMessage: "Cannot perform search by address Only"
          };

        if (field === "postalCd") {
          return {
            warning: "true",
            warningMessage:
              "This search may return many results and be very slow. Add more filters to improve performance"
          };
        }

        if (
          field.includes("Nme") &&
          (operator === "nicknames" || operator === "similar")
        ) {
          return {
            warning: "true",
            warningMessage:
              "This search may return many results and be very slow. Add more filters to improve performance"
          };
        }

        if (
          (field === "firstNme" || field === "anyNme") &&
          (operator === "contains" ||
            operator === "startswith" ||
            operator === "endswith")
        ) {
          return {
            warning: "true",
            warningMessage:
              "This search may return many results and be very slow. Add more filters to improve performance"
          };
        }
      }

      return {
        warning: false,
        warningMessage: null
      };
    },
    handleNewSearch() {
      this.resetError();
      this.resetWarning();

      if (!this.isFormValid()) {
        return false;
      }

      const result = this.validateFilters();
      if (result.error) {
        this.error = true;
        this.errorMessage = result.errorMessage;
        return false;
      } else if (result.warning) {
        this.warning = true;
        this.warningMessage = result.warningMessage;
      }

      this.disableSearch = true;
      this.sort_value = "lastNme";
      this.sort_type = "dsc";
      const queryString = this.generateQueryString(1);

      this.$router
        .push({
          query: qs.parse(queryString)
        })
        .catch(e => {
          if (e && e.name && e.name === "NavigationDuplicated") {
            this.$refs.corpPartyTable.fetchData();
          }
        });
    },
    handleSearch() {
      const queryString = this.generateQueryString();
      this.$router
        .push({
          query: qs.parse(queryString)
        })
        .catch(e => {
          if (e && e.name && e.name !== "NavigationDuplicated") {
            console.error(e);
          }
        });
    },
    renderTable() {
      const queryString = this.generateQueryString();
      this.qs = queryString;
    },
    generateQueryString(page) {
      let queryString =
        buildQueryString(this.filters) +
        `&mode=${this.logic}&additional_cols=${
          this.additional_cols
        }&page=${page || this.page}`;
      if (this.sort_value && this.sort_type) {
        queryString += `&sort_type=${this.sort_type}&sort_value=${this.sort_value}`;
      }

      return queryString;
    },
    init() {
      const {
        mode,
        additional_cols,
        page,
        sort_value,
        sort_type
      } = this.$route.query;

      if (mode) {
        this.logic = mode;
        this.initLogic = mode;
      }

      if (additional_cols) {
        this.additional_cols = additional_cols;
      }

      if (page) {
        this.page = page;
      }

      if (sort_value) {
        this.sort_value = sort_value;
      }

      if (sort_type) {
        this.sort_type = sort_type;
      }

      if (isEmpty(this.$route.query)) {
        this.qs = null;
      } else {
        const queryFilters = Object.assign(
          {},
          omit(
            this.$route.query,
            "mode",
            "additional_cols",
            "page",
            "sort_type",
            "sort_value"
          )
        );

        if (typeof queryFilters.field === "string") {
          queryFilters.uid = this.uid++;
          this.$store.commit("corpParty/filters/setFilters", [queryFilters]);
        } else if (Array.isArray(queryFilters.field)) {
          let temp = [];
          const length = queryFilters.field.length;
          for (let i = 0; i < length; i++) {
            temp.push({
              uid: this.uid++,
              field: queryFilters.field[i],
              operator: queryFilters.operator[i],
              value: queryFilters.value[i]
            });
          }
          this.$store.commit("corpParty/filters/setFilters", temp);
        }
        this.disableSearch = true;
        this.renderTable();
      }
    }
  }
};
</script>

<style lang="scss">
.search-form-container {
  background-color: white;
}
</style>
