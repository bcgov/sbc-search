<template>
  <div>
    <v-container>
      <v-row>
        <v-col
          cols="12"
          class="d-flex justify-space-between align-center mb-12"
        >
          <h2 class="display-1">
            Details for Filing #{{ detail.corp_party_id }}
          </h2>
          <v-icon
            color="#2076d2"
            large
            class="cursor-pointer"
            @click="handlePrint"
            >{{ printerIcon }}</v-icon
          >
        </v-col>
      </v-row>
      <v-row justify="space-between">
        <v-col cols="6">
          <ul class="pa-0 ma-0">
            <li
              v-for="(val, key) in filteredDetail"
              :key="key"
              class="d-flex w-100 detail-list-item"
            >
              <span
                class="font-weight-bold mb-1 detail-key"
                :class="{
                  'detail-big-margins': key === 'cessation_dt' || key === 'addr'
                }"
                >{{ getText(key) }}</span
              >
              <span class="detail-value">{{ val }}</span>
            </li>
          </ul>
        </v-col>
        <v-col cols="6">
          <OfficeTable
            :details="filteredDetail"
            :officesheld="officesheld"
          ></OfficeTable>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { getTextFromValues } from "@/util/index.ts";
import { RESULT_HEADERS } from "@/config/index.js";
import { omit, pick } from "lodash-es";
import { corpPartySearch, corpPartyOfficeSearch } from "@/api/SearchApi.js";
import dayjs from "dayjs";
import OfficeTable from "@/components/Details/OfficeTable.vue";
import { mdiPrinter } from "@mdi/js";
export default {
  components: {
    OfficeTable
  },
  props: {
    detail: {
      default: null,
      type: Object
    },
    officesheld: {
      default: null,
      type: Object
    }
  },
  data() {
    return {
      printerIcon: mdiPrinter
    };
  },
  computed: {
    filteredDetail() {
      const filtered = omit(this.detail, [
        "postal_cd",
        "province",
        "corp_party_id"
      ]);
      if (filtered["appointment_dt"]) {
        filtered["appointment_dt"] = dayjs(filtered["appointment_dt"]).format(
          "YYYY-MM-DD"
        );
      } else {
        filtered["appointment_dt"] = "-";
      }
      if (filtered["cessation_dt"]) {
        filtered["cessation_dt"] = dayjs(filtered["cessation_dt"]).format(
          "YYYY-MM-DD"
        );
      } else {
        filtered["cessation_dt"] = "-";
      }

      filtered["state_typ_cd"] =
        filtered["states"] && filtered["states"][0]["state_typ_cd"];

      return pick(filtered, [
        "last_nme",
        "first_nme",
        "middle_nme",
        "addr",
        "party_typ_cd",
        "appointment_dt",
        "cessation_dt",
        "corp_nme",
        "corp_num",
        "corp_typ_cd",
        "corp_addr",
        "state_typ_cd"
      ]);
    }
  },
  methods: {
    getText(data) {
      return getTextFromValues(RESULT_HEADERS, data);
    },
    handlePrint() {
      window && window.print();
    }
  }
};
</script>

<style lang="scss">
.detail-list-item span {
  flex: 1 1 0;
}
.detail-value {
  color: $COLOR_SECONDARY;
}

.v-application .detail-big-margins {
  margin-bottom: 4em !important;
}
</style>
