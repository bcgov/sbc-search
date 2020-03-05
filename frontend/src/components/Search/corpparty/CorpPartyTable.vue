<template>
  <div>
    <v-data-table
      v-if="qs"
      class="elevation-1 corp-party-table"
      :headers="headers"
      :items="results"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      @update:page="fetchData"
      @update:sort-by="fetchData"
      @update:sort-desc="fetchData"
      :footer-props="{
        'items-per-page-options': [50]
      }"
    >
      <template v-slot:item="{ item }">
        <tr class="cursor-pointer" @click="handleCellClick(item['corp_party_id'])">
          <td class="color-gray">{{ item["corp_party_id"] }}</td>
          <td>{{ item["last_nme"] }}</td>
          <td>{{ item["middle_nme"] }}</td>
          <td>{{ item["first_nme"] }}</td>
          <td>{{ item["appointment_dt"] }}</td>
          <td>{{ item["cessation_dt"] }}</td>
          <td v-if="type === 'active'">{{ item["state_typ_cd"] }}</td>
          <td v-if="type === 'addr'">{{ item["addr"] }}</td>
          <td @click.prevent.stop="handleCorpClick(item['corp_num'])">
            <span class="anchor-text cursor-pointer">{{ item["corp_num"] }}</span>
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { CORPPARTY_HEADERS } from "@/config/index.ts";
import { corpPartySearch } from "@/api/SearchApi.js";
import dayjs from "dayjs";
import { mapGetters } from "vuex";
import { buildQueryString } from "@/util/index.ts";
import { isEmpty } from "lodash-es";

export default {
  props: {
    qs: {
      default: null,
      type: String
    },
    type: {
      default: "none",
      type: String
    }
  },
  computed: {
    headers() {
      return this.filterHeaders(CORPPARTY_HEADERS, this.type);
    },
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
      filters: "corpParty/filters/getFilters",
      numFilters: "corpParty/filters/getNumFilters"
    })
  },
  data() {
    return {
      items: [],
      options: {},
      loading: true,
      totalItems: 0,
      show: false
    };
  },
  methods: {
    handleCorpClick(id) {
      window.open(`#/corporation/${id}`);
    },
    handleCellClick(id) {
      window.open(`#/corpparty/${id}`);
    },
    filterHeaders(headers, type) {
      if (type === "none") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "corp_party_id" ||
            val === "last_nme" ||
            val === "middle_nme" ||
            val === "first_nme" ||
            val === "appointment_dt" ||
            val === "cessation_dt" ||
            val === "corp_num"
          ) {
            return true;
          }
          return false;
        });
      } else if (type === "addr") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "corp_party_id" ||
            val === "last_nme" ||
            val === "middle_nme" ||
            val === "first_nme" ||
            val === "appointment_dt" ||
            val === "cessation_dt" ||
            val === "corp_num" ||
            val === "addr"
          ) {
            return true;
          }
          return false;
        });
      } else if (type === "active") {
        return headers.filter(h => {
          const val = h.value;
          if (
            val === "corp_party_id" ||
            val === "last_nme" ||
            val === "middle_nme" ||
            val === "first_nme" ||
            val === "appointment_dt" ||
            val === "cessation_dt" ||
            val === "corp_num" ||
            val === "state_typ_cd"
          ) {
            return true;
          }
          return false;
        });
      }
    },
    fetchData() {
      if (!this.qs) {
        return;
      }

      this.loading = true;
      const { page, sortBy, sortDesc } = this.options;
      corpPartySearch(this.qs)
        .then(result => {
          this.items = result.data.results;
          this.totalItems = this.items.length;
          this.loading = false;
        })
        .catch(e => {
          this.items = [];
          this.totalItems = 0;
          this.loading = false;
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

<style lang="scss">
.corp-party-table th:first-of-type,
.corp-party-table td:first-of-type {
  color: rgba(0, 0, 0, 0.4) !important;
}
</style>
