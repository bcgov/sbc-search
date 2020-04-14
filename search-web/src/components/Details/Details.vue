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
              title: $vuetify.breakpoint.smAndUp
            }"
          >
            <span class="font-weight-bold"
              >{{ detail.firstNme }} {{ detail.middleNme }}
              {{ detail.lastNme }}</span
            >
            <span v-if="detail.corpNme">
              at
              <span
                class="font-weight-bold cursor-pointer detail-office-link"
                @click="handleCorpClick(detail.corpNum)"
                >{{ detail.corpNme }}
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
          class="subtitle-1"
          :class="{
            'subtitle-1': $vuetify.breakpoint.smAndDown,
            'font-weight-bold': $vuetify.breakpoint.smAndDown
          }"
        >
          {{ detail.fullDesc }}
        </h2>
      </v-row>
      <v-row>
        <h2
          class="pa-0 ma-0 mb-12 subtitle-1 font-weight-regular color-gray detail-filing-number"
        >
          Filing #{{ detail.corpPartyId }}
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
                'detail-big-margins': key === 'cessationDt' || key === 'addr'
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
        "postalCd",
        "province",
        "corpPartyId"
      ]);
      if (filtered["appointmentDt"]) {
        filtered["appointmentDt"] = dayjs(filtered["appointmentDt"]).format(
          "YYYY-MM-DD"
        );
      } else {
        filtered["appointmentDt"] = "-";
      }
      if (filtered["cessationDt"]) {
        filtered["cessationDt"] = dayjs(filtered["cessationDt"]).format(
          "YYYY-MM-DD"
        );
      } else {
        filtered["cessationDt"] = "-";
      }

      filtered["stateTypCd"] =
        filtered["states"] && filtered["states"][0]["stateTypCd"];

      return pick(filtered, [
        "lastNme",
        "firstNme",
        "middleNme",
        "deliveryAddr",
        "mailingAddr",
        "corpPartyEmail",
        "partyTypCd",
        "businessNme",
        "appointmentDt",
        "cessationDt",
        "stateTypCd",
        "corpNme",
        "corpNum",
        "corpTypCd",
        "corpDeliveryAddr",
        "corpMailingAddr",
        "corpAdminEmail"
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
