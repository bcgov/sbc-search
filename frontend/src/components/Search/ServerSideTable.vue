<template>
  <div>
    <v-data-table
      class="elevation-1"
      :headers="headers"
      :items="results"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      @update:page="fetchData"
      @update:sort-by="fetchData"
      @update:sort-desc="fetchData"
      :footer-props="{
        'items-per-page-options': [5]
      }"
    >
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <router-link
              :to="{
                name: 'details',
                query: {
                  corp_party_id: item['corp_party_id']
                }
              }"
              >{{ item["last_nme"] }}</router-link
            >
          </td>
          <td>{{ item["middle_nme"] }}</td>
          <td>{{ item["first_nme"] }}</td>
          <td>{{ item["appointment_dt"] }}</td>
          <td>{{ item["cessation_dt"] }}</td>
          <td></td>
          <td>
            <router-link :to="{ name: 'details', query: item }">{{
              item["corp_num"]
            }}</router-link>
          </td>
          <td>{{ item["corp_nme"] }}</td>
          <td>{{ item["addr_line_1"] }}</td>
        </tr>
      </template>
    </v-data-table>
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
        r["appointment_dt"] = dayjs(r["appointment_dt"]).format("YYYY-MM-DD");
        r["cessation_dt"] = dayjs(r["appointment_dt"]).format("YYYY-MM-DD");
        return r;
      });
    }
  },
  data() {
    return {
      headers: this.filterHeaders(RESULT_HEADERS),
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
    filterHeaders(headers) {
      return headers.filter(h => {
        const val = h.value;
        if (
          val === "corp_party_id" ||
          val === "postal_cd" ||
          val === "province"
        ) {
          return false;
        }
        return true;
      });
    },
    sliceByPage(items, page, itemsPerPage) {
      return items.slice((page - 1) * itemsPerPage, page * itemsPerPage);
    },
    fetchData() {
      this.loading = true;
      const query = this.$route.query;
      const { page, sortBy, sortDesc } = this.options;

      let type = "basic";
      if (query.advanced) {
        type = "advanced";
      }

      let q = query.queryString + `&page=${page}`;
      if (sortDesc.length > 0) {
        const sortOrder = sortDesc[0] ? "desc" : "asc";
        q += `&sort_type=${sortOrder}`;
      }
      if (sortBy.length > 0) {
        q += `&sort_value=${sortBy}`;
      }

      searchApiV2(q, { type })
        .then(result => {
          this.items = result.data.results;
          this.totalItems = result.data.total;
          this.loading = false;
        })
        .catch(e => {
          this.items = [];
          this.totalItems = 0;
          this.loading = false;
          console.error(e);
        });
    }
  }
};
</script>

<style></style>
