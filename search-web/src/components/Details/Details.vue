<template>
  <div class="detail-container">
    <v-container>
      <v-row>
        <v-col
          cols="12"
          class="d-flex detail-header-container justify-space-between align-top pl-0 ma-0 pa-0"
          :class="{
            'flex-wrap': $vuetify.breakpoint.smAndDown
          }"
        >
          <h2
            :class="{
              'pl-0': $vuetify.breakpoint.xsOnly,
              'display-1': $vuetify.breakpoint.smAndUp
            }"
          >
            <span class="font-weight-bold"
              >{{ detail.first_nme }} {{ detail.middle_nme }}
              {{ detail.last_nme }}</span
            >
            <span v-if="detail.corp_nme">
              at
              <span
                class="font-weight-bold cursor-pointer detail-office-link"
                @click="handleCorpClick(detail.corp_num)"
                >{{ detail.corp_nme }}
              </span></span
            >
          </h2>
          <PrintButton
            :class="{
              'pt-5': $vuetify.breakpoint.smAndDown,
              'pl-5': $vuetify.breakpoint.mdAndUp
            }"
          ></PrintButton>
        </v-col>
      </v-row>
      <v-row>
        <h2
          :class="{
            title: $vuetify.breakpoint.smAndDown,
            'font-weight-bold': $vuetify.breakpoint.smAndDown
          }"
        >
          {{ detail.full_desc }}
        </h2>
      </v-row>
      <v-row>
        <h2
          class="pa-0 ma-0 mb-12 title font-weight-regular color-gray detail-filing-number"
        >
          Filing #{{ detail.corp_party_id }}
        </h2>
      </v-row>

      <v-row>
        <ul class="pa-0 ma-0 detail-list">
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
      </v-row>
      <v-row>
        <OfficeTable
          :details="filteredDetail"
          :officesheld="officesheld"
          class="mt-10 w-100"
        ></OfficeTable>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import PrintButton from "@/components/PrintButton.vue";
import { getTextFromValues } from "@/util/index.ts";
import { CORPPARTY_HEADERS } from "@/config/index.ts";
import pick from "lodash-es/pick";
import omit from "lodash-es/omit";
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
    },
    handleCorpClick(id) {
      window.open(`/corporation/${id}`);
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

.detail-office-link {
  border-bottom: 2px solid black;
}

.detail-list {
  width: 100%;
}
</style>
