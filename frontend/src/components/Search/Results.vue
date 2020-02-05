<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="searchResults"
      :items-per-page="10"
      class="elevation-1 result-table"
      @click.native="handleTableClick"
    >
    </v-data-table>
  </div>
</template>

<script>
import { RESULT_HEADERS } from "@/plugins/config.js";
export default {
  props: {
    searchResults: {
      default: function() {
        return [];
      },
      type: Array
    }
  },
  methods: {
    handleTableClick(e) {
      // Column 0 => Last Name
      // Column 6 => Org Number
      console.log(e);
      const column = e.target.cellIndex;
      if (column === 0) {
        return this.$router.push({
          name: "details"
        });
      }

      if (column === 6) {
        return this.$router.push({
          name: "details"
        });
      }
    }
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
</style>
