<template>
  <div>
    <v-data-table
      v-if="qs"
      mobile-breakpoint="960"
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
      <template v-slot:item="{ item, index, headers }">
        <!-- Mobile View Begin -->
        <tr
          class="cursor-pointer d-table-row d-md-none mobile-tr-row"
          v-for="(value, i) in Object.values(orderItems(item))"
          :key="`row${index}${value}${i}`"
        >
          <td
            v-if="headers[i].value === 'corpNum'"
            class="d-table-cell"
            @click.prevent.stop="handleCorpClick(item['corpNum'])"
          >
            <div class="d-flex w-100 justify-space-between">
              <div class="color-black">{{ headers[i].text }}</div>
              <div class="text-right anchor-text cursor-pointer">
                {{ value }}
              </div>
            </div>
          </td>
          <td
            v-else
            class="d-table-cell"
            @click="handleCellClick(item['corpPartyId'])"
          >
            <div class="d-flex w-100 justify-space-between">
              <div class="color-black">{{ headers[i].text }}</div>
              <div class="text-right">{{ value }}</div>
            </div>
          </td>
        </tr>
        <v-divider class="d-md-none" />
        <!-- Mobile View End -->

        <tr
          class="cursor-pointer d-none d-md-table-row"
          @click="handleCellClick(item['corpPartyId'])"
        >
          <td class="color-gray">{{ item["corpPartyId"] }}</td>
          <td>{{ item["lastNme"] }}</td>
          <td>{{ item["firstNme"] }}</td>
          <td>{{ item["middleNme"] }}</td>
          <td>{{ item["addr"] }}</td>
          <td>{{ item["postalCd"] }}</td>
          <td>{{ item["partyTypCd"] }}</td>
          <td>{{ item["appointmentDt"] }}</td>
          <td>{{ item["cessationDt"] }}</td>
          <td>{{ item["stateTypCd"] }}</td>
          <td>{{ item["corpNme"] }}</td>
          <td @click.prevent.stop="handleCorpClick(item['corpNum'])">
            <span class="anchor-text cursor-pointer">{{
              item["corpNum"]
            }}</span>
          </td>
        </tr>
      </template>
      <template v-slot:footer>
        <v-progress-linear
          :active="loading"
          :indeterminate="true"
          color="primary"
          height="2"
        ></v-progress-linear>
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
import pick from "lodash-es/pick";
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
        if (r["appointmentDt"]) {
          r["appointmentDt"] = dayjs(r["appointmentDt"]).format("YYYY-MM-DD");
        } else {
          r["appointmentDt"] = "-";
        }

        if (r["cessationDt"]) {
          r["cessationDt"] = dayjs(r["cessationDt"]).format("YYYY-MM-DD");
        } else {
          r["cessationDt"] = "-";
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
    orderItems(items) {
      return pick(items, [
        "corpPartyId",
        "lastNme",
        "firstNme",
        "middleNme",
        "addr",
        "postalCd",
        "partyTypCd",
        "appointmentDt",
        "cessationDt",
        "stateTypCd",
        "corpNme",
        "corpNum"
      ]);
    },
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
          val === "corpPartyId" ||
          val === "lastNme" ||
          val === "middleNme" ||
          val === "firstNme" ||
          val === "partyTypCd" ||
          val === "appointmentDt" ||
          val === "cessationDt" ||
          val === "corpNum" ||
          val === "corpNme" ||
          val === "stateTypCd" ||
          val === "addr" ||
          val === "postalCd"
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

.mobile-tr-row,
.mobile-tr-row td {
  border-bottom: 0 !important;
}
</style>
