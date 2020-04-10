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
        @search="handleSearch"
        :class="{
          'mb-n6': $vuetify.breakpoint.smAndUp
        }"
      ></CorporationSearch>
    </div>

    <div
      v-if="!isQueryEmpty"
      class="d-flex justify-space-between align-center mb-5"
    >
      <h4 class="headline">Search Results</h4>
      <v-btn
        class="export-btn body-1 color-dark-grey border-gray"
        height="50"
        @click="handleExport"
        :elevation="0"
        >Export to .xlsx</v-btn
      >
    </div>
    <CorporationTable
      ref="corporationTable"
      :page="page"
      :query="query"
      @pageUpdate="handlePageUpdate"
      @sortUpdate="handleSortUpdate"
    ></CorporationTable>
  </div>
</template>

<script>
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";
import { corporationSearch, EXPORT_CORPORATION_URL } from "@/api/SearchApi.js";
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
      query: null,
      page: "1",
      sort_value: "corpNme",
      sort_type: "dsc"
    };
  },
  methods: {
    handleSearch(searchQuery) {
      this.page = "1";
      const query = {
        query: searchQuery,
        page: 1,
        sort_type: "dsc",
        sort_value: "corpNme"
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
      this.$router.push({ query });
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
    handleExport() {
      const datetime = dayjs().format("YYYY-MM-DD HH:mm:ss");
      downloadFile(
        `${
          process.env.VUE_APP_BACKEND_HOST
        }${EXPORT_CORPORATION_URL}/?${qs.stringify(this.$route.query)}`,
        `Corporation Search Results ${datetime}.xlsx`
      );
    }
  },
  mounted() {
    if (!this.isQueryEmpty && this.$route.query.query) {
      const query = this.$route.query;
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
