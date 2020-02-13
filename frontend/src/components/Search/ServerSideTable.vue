<template>
  <div>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      :items="results"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      @update:items-per-page="fetchData"
      @click.native="handleTableClick"
      @update:page="fetchData"
      :footer-props="{
        'items-per-page-options': [20]
      }"
    >
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <router-link :to="{ name: 'details', query: item }">{{
              item["LAST_NME"]
            }}</router-link>
          </td>
          <td>{{ item["MIDDLE_NME"] }}</td>
          <td>{{ item["FIRST_NME"] }}</td>
          <td>{{ item["APPOINTMENT_DT"] }}</td>
          <td>{{ item["CESSATION_DT"] }}</td>
          <td></td>
          <td>
            <router-link :to="{ name: 'details', query: item }">{{
              item["CORP_NUM"]
            }}</router-link>
          </td>
          <td>{{ item["CORP_NME"] }}</td>
          <td>{{ item["ADDR_LINE_1"] }}</td>
        </tr>
      </template>
    </v-data-table>
    {{ options }}
  </div>
</template>

<script>
import { RESULT_HEADERS } from "@/plugins/config.js";
import { searchApiV2 } from "@/plugins/SearchApi.js";
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
      this.loading = true;
      const query = this.$route.query;
      const { page } = this.options;

      let type = "basic";
      if (query.advanced) {
        type = "advanced";
      }

      let q = query.queryString + `&page=${page}`;
      console.log(q);

      searchApiV2(q, { type }).then(result => {
        this.items = result.data.results;

        this.totalItems = result.data.total;
        this.loading = false;
      });
    }
  }
};
</script>

<style></style>
