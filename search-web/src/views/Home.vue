<template>
  <div class="home">
    <h1>Welcome to Director Search.</h1>
    <h4 class="mt-3 body-1 mb-10">
      Search for offices held at active and historical BC companies.
    </h4>

    <div class="pa-10 search-form-container">
      <SearchTips></SearchTips>
      <v-form>
        <div v-for="(criteria, index) in filters" :key="index">
          <CorpPartySearch
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
          ></SearchLogic>
          <SbcButton
            class="d-inline-block"
            type="submit"
            title="Search"
            @click.native.prevent="handleNewSearch"
          ></SbcButton>
        </div>
      </v-form>
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
        <v-btn class="export-btn" height="50" @click="handleExport"
          >Export to .xlsx</v-btn
        >
      </div>
      <CorpPartyTable
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

import omit from "lodash-es/omit";
import isEmpty from "lodash-es/isEmpty";
const qs = require("qs");
import { searchApi } from "@/api/SearchApi";
import CorpPartyTable from "@/components/Search/corpparty/CorpPartyTable.vue";
import { buildQueryString } from "@/util/index.ts";
import SearchLogic from "@/components/Search/corpparty/SearchLogic.vue";
import SearchTips from "@/components/Search/corpparty/SearchTips.vue";
import { BACKEND_URL } from "@/config/index.ts";
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
      uid: 1,
      searchQuery: null,
      logic: "ALL",
      qs: null,
      additional_cols: "none",
      page: "1",
      sort_value: null,
      sort_type: null
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
    handleExport() {
      const queryString = this.generateQueryString();
      window.open(`${BACKEND_URL}/person/search/export/?${queryString}`);
    },
    handlePageUpdate(page) {
      this.page = page;
      this.handleSearch();
    },
    handleSortUpdate(options) {
      this.sort_value = options.sortBy[0];
      if (options.sortDesc.length > 0) {
        this.sort_type = options.sortDesc[0] ? "dsc" : "asc";
      } else {
        this.sort_type = null;
      }
      this.handleSearch();
    },
    handleColumnClick(type) {
      const query = Object.assign({}, this.$route.query);
      query.additional_cols = type;
      this.additional_cols = type;
      this.$router.push({
        query
      });
    },
    addFilter(event, field = "first_nme", operator = "contains", value = "") {
      this.uid++;
      this.$store.commit("corpParty/filters/addFilter", {
        uid: this.uid,
        field,
        operator,
        value
      });
    },
    handleNewSearch() {
      this.sort_value = "last_nme";
      this.sort_type = "dsc";
      const queryString = this.generateQueryString(1);

      this.$router.push({
        query: qs.parse(queryString)
      });
    },
    handleSearch() {
      const queryString = this.generateQueryString();
      this.$router.push({
        query: qs.parse(queryString)
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
      const mode = this.$route.query.mode;
      const additional_cols = this.$route.query.additional_cols;
      const page = this.$route.query.page;
      const sort_value = this.$route.query.sort_value;
      const sort_type = this.$route.query.sort_type;

      if (mode) {
        this.logic = mode;
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
        const queryFilters = omit(
          this.$route.query,
          "mode",
          "additional_cols",
          "page",
          "sort_type",
          "sort_value"
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
