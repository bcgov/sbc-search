<template>
  <div>
    <v-data-table
      v-if="query"
      class="corporation-table"
      mobile-breakpoint="960"
      :loading="loading"
      :headers="headers"
      :options.sync="options"
      :disable-sort="disableSorting"
      :items="corporations"
      @update:sort-by="updateSort"
      @update:sort-desc="updateSort"
      :sort-by="sortBy"
      :sort-desc="sortDesc"
      :footer-props="{
        'items-per-page-options': [50]
      }"
    >
      <template v-slot:top="{ pagination }">
        <div class="v-data-footer v-data-custom-header">
          <div
            v-if="corporations.length === 0"
            class="v-data-footer__pagination"
          >
            -
          </div>
          <div v-else class="v-data-footer__pagination">
            <div class="custom-footer d-flex align-center">
              <div>Showing {{ pagination.itemsLength }} results</div>
              <div class="d-flex ml-5 align-center">
                <v-btn
                  v-if="page > '1' && !loading"
                  icon
                  @click="pagePrev"
                  small
                >
                  <v-icon>arrow_back</v-icon>
                </v-btn>
                <v-btn v-else disabled icon small>
                  <v-icon>arrow_back</v-icon>
                </v-btn>
                <div class="d-inline-block mr-3 ml-3">Page {{ page }}</div>
                <v-btn
                  icon
                  v-if="corporations.length > 49 && !loading"
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
          </div>
        </div>
      </template>
      <template v-slot:item="{ item, index, headers }">
        <!-- Mobile View Begin -->
        <tr
          @click="handleTableRowClick(item, $event)"
          class="cursor-pointer d-table-row d-md-none mobile-tr-row"
          v-for="(value, i) in Object.values(orderItems(item))"
          :key="`row${index}${value}${i}`"
        >
          <td class="d-table-cell">
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
          @click="handleTableRowClick(item, $event)"
        >
          <td class="anchor-text">{{ item["corpNum"] }}</td>
          <td>{{ item["corpTypCd"] }}</td>
          <td>{{ item["corpNme"] }}</td>
          <td>{{ formatDate(item["recognitionDts"]) }}</td>
          <td>{{ item["stateTypCd"] }}</td>
          <td>{{ item["addr"] }}</td>
          <td>{{ item["postalCd"] }}</td>
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
              v-if="corporations.length > 49 && !loading"
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
import { CORPORATION_HEADERS } from "@/config/index.ts";
import { corporationSearch } from "@/api/SearchApi";
import dayjs from "dayjs";
import { formatDate } from "@/util/index.ts";
import pick from "lodash-es/pick";

export default {
  props: {
    query: {
      default: null,
      type: Object
    },
    page: {
      default: "1",
      type: String
    }
  },
  data() {
    return {
      headers: CORPORATION_HEADERS,
      corporations: [],
      loading: false,
      totalItems: 0,
      options: {},
      disableSorting: false,
      sortBy: [],
      sortDesc: []
    };
  },
  methods: {
    formatDate,
    orderItems(items) {
      return pick(items, [
        "corpNum",
        "corpTypCd",
        "corpNme",
        "recognitionDts",
        "stateTypCd",
        "addr",
        "postalCd"
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
    handleTableRowClick(item, e) {
      e.target.closest("tr").classList.add("row-clicked");
      window.open(`/corporation/${item["corpNum"]}`);
    },
    async fetchData(query) {
      const { sort_type, sort_value } = query;
      this.sortBy = [sort_value];
      if (sort_type === "asc") {
        this.sortDesc = [false];
      } else if (sort_type === "dsc") {
        this.sortDesc = [true];
      }

      this.loading = true;
      this.disableSorting = true;

      corporationSearch(query)
        .then(result => {
          this.corporations = result.data.results;
          this.totalItems = this.corporations.length;
          this.loading = false;
          this.disableSorting = false;
          this.$emit("success", result);
        })
        .catch(e => {
          this.$emit("error", e);
          this.corporations = [];
          this.totalItems = 0;
          this.disableSorting = false;
          this.loading = false;
        });
    }
  },
  watch: {
    query(nq) {
      this.fetchData(nq);
    }
  }
};
</script>
<style lang="scss">
.corporation-table .custom-footer {
  padding: 1em 0;
}

.corporation-table .v-data-footer__icons-after,
.corporation-table .v-data-footer__icons-before {
  display: none;
}

.v-data-custom-header {
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.row-clicked {
  background-color: $COLOR_LAVENDER !important;
}
</style>
