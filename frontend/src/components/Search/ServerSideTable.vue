<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="results"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      class="elevation-1"
      @update:items-per-page="fetchData"
      @update:page="fetchData"
    ></v-data-table>
    {{ options }}
  </div>
</template>

<script>
import { RESULT_HEADERS } from "@/plugins/config.js";
import { searchApi, advancedSearchApi } from "@/plugins/SearchApi.js";
import dayjs from "dayjs";

export default {
  computed: {
    results() {
      return this.items.map(r => {
        r["APPOINTMENT_DT"] = dayjs(r["APPOINTMENT_DT"]).format("YYYY-MM-DD");
        r["CESSATION_DT"] = dayjs(r["APPOINTMENT_DT"]).format("YYYY-MM-DD");
        return r;
      });
    }
  },
  data() {
    return {
      headers: RESULT_HEADERS,
      items: [],
      options: {},
      loading: true,
      totalItems: 0
    };
  },
  async mounted() {
    this.fetchData();
  },
  methods: {
    sliceByPage(items, page, itemsPerPage) {
      return items.slice((page - 1) * itemsPerPage, page * itemsPerPage);
    },
    fetchData() {
      const query = this.$route.query;
      const { page, itemsPerPage } = this.options;
      if (!query.advanced) {
        const searchParams = {
          page: query.page,
          query: query.searchQuery
        };
        searchApi(searchParams).then(result => {
          this.items = result.data.results;
          if (itemsPerPage > 0) {
            this.items = this.sliceByPage(
              result.data.results,
              page,
              itemsPerPage
            );
          }
          this.totalItems = result.data.results.length;
          this.loading = false;
        });
      } else {
        const queryString = query.queryString;
        advancedSearchApi(queryString).then(result => {
          this.items = result.data.results;
          if (itemsPerPage > 0) {
            this.items = this.sliceByPage(
              result.data.results,
              page,
              itemsPerPage
            );
          }
          this.totalItems = result.data.results.length;
          this.loading = false;
        });
      }
    }
  }
};
</script>

<style></style>
