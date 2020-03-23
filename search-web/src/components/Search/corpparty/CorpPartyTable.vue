<template>
  <div>
    <v-data-table
      v-if="qs"
      :calculate-widths="true"
      class="elevation-1 corp-party-table"
      :headers="headers"
      :items="results"
      :options.sync="options"
      :server-items-length="totalItems"
      :loading="loading"
      :disable-sort="disableSorting"
      @update:sort-by="updateSort"
      @update:sort-desc="updateSort"
      :sort-by="sortBy"
      :sort-desc="sortDesc"
      :footer-props="{
        'items-per-page-options': [20]
      }"
    >
      <template v-slot:item="{ item }">
        <tr
          class="cursor-pointer"
          @click="handleCellClick(item['corp_party_id'])"
        >
          <td class="color-gray">{{ item["corp_party_id"] }}</td>
          <td>{{ item["last_nme"] }}</td>
          <td>{{ item["first_nme"] }}</td>
          <td>{{ item["middle_nme"] }}</td>
          <td>{{ item["addr"] }}</td>
          <td>{{ item["postal_cd"] }}</td>
          <td>{{ item["party_typ_cd"] }}</td>
          <td>{{ item["appointment_dt"] }}</td>
          <td>{{ item["cessation_dt"] }}</td>
          <td>{{ item["state_typ_cd"] }}</td>
          <td>{{ item["corp_nme"] }}</td>
          <td @click.prevent.stop="handleCorpClick(item['corp_num'])">
            <span class="anchor-text cursor-pointer">{{
              item["corp_num"]
            }}</span>
          </td>
        </tr>
      </template>
      <template v-slot:footer.page-text="{ itemsLength }">
        <div class="custom-footer d-flex align-center">
          <div>Showing {{ itemsLength }} results</div>
          <div class="d-flex ml-5 align-center">
            <v-btn v-if="page > '1' && !loading" icon @click="pagePrev" small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <v-btn v-else disabled icon small>
              <v-icon>arrow_back</v-icon>
            </v-btn>
            <div class="d-inline-block mr-3 ml-3">Page {{ page }}</div>
            <v-btn
              icon
              v-if="results.length > 19 && !loading"
              @click="pageNext"
              small
            >
              <v-icon>arrow_forward</v-icon>
            </v-btn>
            <v-btn icon v-else disabled small>
              <v-icon>arrow_forward</v-icon>
            </v-btn>
          </div>
        </div>
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
import isEmpty from "lodash-es/isEmpty";
const qsl = require("qs");
export default {
  props: {
    qs: {
      default: null,
      type: String
    },
    type: {
      default: "none",
      type: String
    },
    page: {
      default: "1",
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
      disableSorting: false,
      sortBy: [],
      sortDesc: []
    };
  },
  methods: {
    pageNext() {
      this.$emit("pageUpdate", (parseInt(this.page) + 1).toString());
    },
    pagePrev() {
      if (this.page > "1") {
        this.$emit("pageUpdate", (parseInt(this.page) - 1).toString());
      }
    },
    updateSort() {
      this.$emit("sortUpdate", {
        sortBy: this.options.sortBy,
        sortDesc: this.options.sortDesc
      });
    },
    handleCorpClick(id) {
      window.open(`/corporation/${id}`);
    },
    handleCellClick(id) {
      if (window.getSelection().toString()) {
        return;
      }
      window.open(`/corpparty/${id}`);
    },
    filterHeaders(headers, type) {
      return headers.filter(h => {
        const val = h.value;
        if (
          val === "corp_party_id" ||
          val === "last_nme" ||
          val === "middle_nme" ||
          val === "first_nme" ||
          val === "party_typ_cd" ||
          val === "appointment_dt" ||
          val === "cessation_dt" ||
          val === "corp_num" ||
          val === "corp_nme" ||
          val === "state_typ_cd" ||
          val === "addr" ||
          val === "postal_cd"
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
      this.disableSorting = true;
      let queryString = this.qs;
      const { sort_type, sort_value } = qsl.parse(queryString);
      if (sort_type && sort_value) {
        this.sortBy = [sort_value];
        if (sort_type === "asc") {
          this.sortDesc = [false];
        } else if (sort_type === "dsc") {
          this.sortDesc = [true];
        }
      }

      corpPartySearch(queryString)
        .then(result => {
          this.items = result.data.results;
          this.totalItems = this.items.length;
          this.loading = false;
          this.disableSorting = false;
        })
        .catch(e => {
          this.items = [];
          this.totalItems = 0;
          this.loading = false;
          this.disableSorting = false;
        });
    }
  },
  watch: {
    qs(nq) {
      this.fetchData();
    }
  }
};
</script>

<style lang="scss">
.corp-party-table th:first-of-type,
.corp-party-table td:first-of-type {
  color: rgba(0, 0, 0, 0.6) !important;
}

.corp-party-table .custom-footer {
  padding: 1em 0;
}

.corp-party-table .v-data-footer__icons-after,
.corp-party-table .v-data-footer__icons-before {
  display: none;
}
.corp-party-table th span {
}
</style>
