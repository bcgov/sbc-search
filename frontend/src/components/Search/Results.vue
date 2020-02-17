<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="results"
      :items-per-page="10"
      class="elevation-1 result-table"
      @click:row="handleRowClick"
    >
    </v-data-table>
  </div>
</template>

<script>
import { RESULT_HEADERS } from "@/plugins/config.js";
import dayjs from "dayjs";

export default {
  props: {
    searchResults: {
      default: function() {
        return [];
      },
      type: Array
    }
  },
  computed: {
    results() {
      return this.searchResults.map(r => {
        r["appointment_dt"] = dayjs(r["appointment_dt"]).format("YYYY-MM-DD");
        r["cessation_dt"] = dayjs(r["appointment_dt"]).format("YYYY-MM-DD");
        return r;
      });
    }
  },
  methods: {
    handleRowClick(data) {
      return this.$router.push({
        name: "details",
        query: data
      });
    },
    handleTableClick() {}
  },
  data() {
    return {
      headers: RESULT_HEADERS
    };
  }
};
</script>

<style lang="sass">
.result-table tbody tr td:first-of-type,
.result-table tbody tr td:nth-of-type(7)
  text-decoration: underline
  color: #2a7cd4
  cursor: pointer

.result-table tbody tr td:nth-of-type(4),
.result-table tbody tr td:nth-of-type(5)
  width: 120px
  white-space: nowrap

.result-table
  white-space: nowrap
</style>
