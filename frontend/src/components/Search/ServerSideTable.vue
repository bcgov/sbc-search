<template>
  <div>
    <v-data-table
      v-if="qs"
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
        'items-per-page-options': [20]
      }"
    >
      <template v-slot:item="{ item }">
        <tr>
          <td>
            <a
              :href="`#/details?corp_party_id=${item['corp_party_id']}`"
              target="_blank"
              >{{ item["last_nme"] }}</a
            >
          </td>
          <td>{{ item["middle_nme"] }}</td>
          <td>{{ item["first_nme"] }}</td>
          <td>{{ item["appointment_dt"] }}</td>
          <td>{{ item["cessation_dt"] }}</td>
          <td>
            <a
              :href="`#/details?corp_party_id=${item['corp_party_id']}`"
              target="_blank"
              >{{ item["corp_num"] }}</a
            >
          </td>
          <td>{{ item["corp_nme"] }}</td>

          <td>
            <a
              :href="`#/details?corp_party_id=${item['corp_party_id']}`"
              target="_blank"
              >{{ item["corp_party_id"] }}</a
            >
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { RESULT_HEADERS } from "@/config/index.js";
import { searchApi } from "@/api/SearchApi.js";
import dayjs from "dayjs";
import { mapGetters } from "vuex";
import { buildQueryString } from "@/util/index.ts";
import { isEmpty } from "lodash-es";

export default {
  props: {
    qs: {
      default: null,
      type: String
    }
  },
  computed: {
    results() {
      return this.items.map(r => {
        if (r["appointment_dt"]) {
          r["appointment_dt"] = dayjs(r["appointment_dt"]).format("YYYY-MM-DD");
        } else {
          r["appointment_dt"] = "-";
        }

        if (r["cessation_dt"]) {
          r["cessation_dt"] = dayjs(r["cessation_dt"]).format("YYYY-MM-DD");
        } else {
          r["cessation_dt"] = "-";
        }

        return r;
      });
    },
    ...mapGetters({
      filters: "filters/getFilters",
      numFilters: "filters/getNumFilters"
    })
  },
  data() {
    return {
      headers: this.filterHeaders(RESULT_HEADERS),
      items: [],
      options: {},
      loading: true,
      totalItems: 0,
      show: false
    };
  },
  methods: {
    filterHeaders(headers) {
      return headers.filter(h => {
        const val = h.value;
        if (
          val === "last_nme" ||
          val === "middle_nme" ||
          val === "first_nme" ||
          val === "appointment_dt" ||
          val === "cessation_dt" ||
          val === "corp_num" ||
          val === "addr" ||
          val === "corp_party_id"
        ) {
          return true;
        }
        return false;
      });
    },
    fetchData() {
      if (!this.qs) {
        return;
      }

      this.loading = true;
      const { page, sortBy, sortDesc } = this.options;

      searchApi(this.qs)
        .then(result => {
          this.items = result.data.results;
          this.totalItems = this.items.length;
          this.loading = false;
        })
        .catch(e => {
          this.items = [];
          this.totalItems = 0;
          this.loading = false;
          console.error(e);
        });
    }
  },
  watch: {
    qs(nq) {
      this.show = true;
      this.fetchData();
    }
  }
};
</script>

<style></style>
