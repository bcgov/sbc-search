<template>
  <div>
    <v-data-table
      class="corporation-table"
      :loading="loading"
      :headers="headers"
      :items="corporations"
      :footer-props="{
        'items-per-page-options': [20]
      }"
    >
      <template v-slot:item="{ item }">
        <tr class="cursor-pointer" @click="handleTableRowClick(item)">
          <td class="anchor-text">{{ item["corp_num"] }}</td>
          <td>{{ item["corp_typ_cd"] }}</td>
          <td>{{ item["corp_nme"] }}</td>
          <td>{{ item["recognition_dts"] }}</td>
          <td>{{ item["state_typ_cd"] }}</td>
          <td>{{ item["addr"] }}</td>
          <td>{{ item["postal_cd"] }}</td>
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
              v-if="corporations.length > 19 && !loading"
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
      totalItems: 0
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
    handleTableRowClick(item) {
      window.open(`/corporation/${item["corp_num"]}`);
    },
    fetchData(query) {
      console.log("query", query);
      this.loading = true;
      corporationSearch(query)
        .then(result => {
          this.corporations = result.data.results;
          this.totalItems = this.corporations.length;
          this.loading = false;
        })
        .catch(e => {
          this.corporations = [];
          this.totalItems = 0;
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
</style>
