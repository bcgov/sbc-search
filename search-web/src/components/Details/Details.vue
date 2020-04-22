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
        <ul class="pa-0 ma-0 detail-list mb-10">
          <li
            v-for="(val, key) in generalInformation"
            :key="key"
            class="d-flex w-100 detail-list-item"
          >
            <span class="font-weight-bold mb-1 detail-key">{{
              getText(key)
            }}</span>
            <span class="middle-border"></span>
            <span class="detail-value">{{ val }}</span>
          </li>
        </ul>
      </v-row>
      <v-row class="mt-10 mb-10">
        <h5 class="body-1 mb-5">Company Information</h5>
        <ul class="pa-0 ma-0 detail-list">
          <li
            v-for="(val, key) in companyInformation"
            :key="key"
            class="d-flex w-100 detail-list-item"
          >
            <span class="font-weight-bold mb-1 detail-key">{{
              getText(key)
            }}</span>
            <span class="middle-border"></span>
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

      const includedFields = [
        "lastNme",
        "firstNme",
        "middleNme",
        "deliveryAddr",
        "mailingAddr",
        "corpPartyEmail",
        "partyTypCd",
        "appointmentDt",
        "cessationDt",
        "stateTypCd",
        "corpNme",
        "corpNum",
        "corpTypCd",
        "corpDeliveryAddr",
        "corpMailingAddr",
        "corpAdminEmail"
      ];

      if (this.detail.hasOwnProperty("businessNme")) {
        includedFields.push("businessNme");
      }

      return pick(filtered, includedFields);
    },
    companyInformation() {
      return pick(this.filteredDetail, [
        "stateTypCd",
        "corpNme",
        "corpNum",
        "corpTypCd",
        "corpDeliveryAddr",
        "corpMailingAddr",
        "corpAdminEmail"
      ]);
    },
    generalInformation() {
      const includedFields = {};
      return pick(this.filteredDetail, [
        "lastNme",
        "firstNme",
        "middleNme",
        "deliveryAddr",
        "mailingAddr",
        "corpPartyEmail",
        "partyTypCd",
        "appointmentDt",
        "cessationDt"
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
  max-width: 1200px;
  width: 100%;
}

.detail-value:after {
  content: ".";
  visibility: hidden;
}
.detail-key {
  flex: 0.5 1 0;
}
.detail-value {
  flex: 1 1 0;
  padding-left: 3em;
}
.middle-border {
  flex: 0.001 !important;
  width: 1px;
  background-color: rgba(0, 0, 0, 0.2);
}

@media only screen and (max-width: 960px) {
  .detail-key,
  .detail-value {
    font-size: 14px !important;
    flex: 1 1 0;
  }
  .detail-value {
    flex: 1.25 1 0;
    padding-left: 1em;
  }
}

@media only screen and (max-width: 600px) {
  .detail-key,
  .detail-value {
    font-size: 12px !important;
    flex: 1.3 1 0;
  }
  .detail-value {
    flex: 1.25 1 0;
    padding-left: 1em;
  }
}
</style>
