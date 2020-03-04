<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12" class="d-flex justify-space-between align-center mb-12">
          <h2 class="display-1">Details for Filing #{{ detail.corp_party_id }}</h2>
          <PrintButton></PrintButton>
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
              >{{ getText(key) }}</span>
              <span class="detail-value">{{ val }}</span>
            </li>
          </ul>
        </v-col>
        <v-col cols="6">
          <OfficeTable :details="filteredDetail" :officesheld="officesheld"></OfficeTable>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import PrintButton from "@/components/PrintButton.vue";
import { getTextFromValues } from "@/util/index.ts";
import { CORPPARTY_HEADERS } from "@/config/index.ts";
import { omit, pick } from "lodash-es";
import { corpPartySearch, corpPartyOfficeSearch } from "@/api/SearchApi.js";
import dayjs from "dayjs";
import OfficeTable from "@/components/Details/OfficeTable.vue";
export default {
  components: {
    OfficeTable,
    PrintButton
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
        "delivery_addr",
        "mailing_addr",
        "corp_party_email",
        "party_typ_cd",
        "appointment_dt",
        "cessation_dt",
        "state_typ_cd",
        "corp_nme",
        "corp_num",
        "corp_typ_cd",
        "corp_delivery_addr",
        "corp_mailing_addr",
        "corp_admin_email"
      ]);
    }
  },
  methods: {
    getText(data) {
      return getTextFromValues(CORPPARTY_HEADERS, data);
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
