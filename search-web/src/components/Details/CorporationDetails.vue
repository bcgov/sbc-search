<template>
  <div>
    <v-container>
      <v-row class="mb-10">
        <v-col cols="12">
          <div
            class="d-flex justify-space-between align-center"
            :class="{
              'flex-wrap': $vuetify.breakpoint.smAndDown
            }"
          >
            <h2
              class="body-1 font-weight-bold crp-details-header"
              :class="{
                'w-100': $vuetify.breakpoint.smAndDown
              }"
            >
              Corporation Details for Inc. #<span class="details-corp-number">{{
                details.corpNum
              }}</span>
            </h2>
            <PrintButton
              :class="{
                'mt-5': $vuetify.breakpoint.smAndDown
              }"
            ></PrintButton>
          </div>
          <CorporationFilings :corpNum="details.corpNum"></CorporationFilings>
        </v-col>
      </v-row>
      <v-row justify="space-between">
        <v-col xs="12" sm="12" md="12" lg="6">
          <ul class="pa-0 ma-0 detail-list">
            <li class="d-flex w-100 detail-list-item mb-5">
              <span class="detail-key font-weight-bold">Company Name(s)</span>
              <span class="middle-border"></span>
              <div class="detail-value">
                <span
                  v-for="(name, index) in details.names"
                  :key="'company' + index"
                  >{{ index + 1 }}. {{ name.name }}</span
                >
              </div>
            </li>
            <li
              class="d-flex w-100 detail-list-item"
              v-for="(val, key) in filteredDetail"
              :key="key + val"
            >
              <span class="detail-key font-weight-bold">
                {{ getText(key) }}
              </span>
              <span class="middle-border"></span>
              <span class="detail-value">{{ val }}</span>
            </li>
            <li class="mb-10"></li>
            <li class="d-flex w-100 detail-list-item mb-5">
              <span class="detail-key font-weight-bold">Office(s)</span>
            </li>
            <li
              class="mb-5"
              v-for="(office, index) in details.offices"
              :key="'office' + index"
            >
              <p>
                (please see Corporate Online for office location details)
              </p>
              <div class="d-flex w-100 detail-list-item">
                <span class="detail-key font-weight-bold">Email</span>
                <span class="detail-value">
                  (not specified)
                </span>
                <span class="detail-value" v-if="office.emailAddress">
                  {{ office.emailAddress }}
                </span>
              </div>
            </li>
          </ul>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import PrintButton from "@/components/PrintButton.vue";
import { getTextFromValues } from "@/util/index.ts";
import { COMPANY_HEADERS } from "@/config/index.ts";
import pick from "lodash-es/pick";
import CorporationFilings from "@/components/Details/CorporationFilings.vue";
export default {
  components: {
    CorporationFilings,
    PrintButton
  },
  props: {
    details: {
      default: null,
      type: Object
    }
  },
  computed: {
    filteredDetail() {
      return pick(this.details, ["corpNum", "stateTypCd", "adminEmail"]);
    }
  },
  methods: {
    getText(data) {
      return getTextFromValues(COMPANY_HEADERS, data);
    }
  }
};
</script>
<style lang="scss">
.detail-list {
  list-style-type: none;
}

.detail-value,
.detail-key {
  flex: 1 1 0;
}

.v-application .detail-big-margins {
  margin-bottom: 4em !important;
}
.detail-key {
  flex: 0.7 1 0;
  line-height: 30px;
}
.detail-value {
  flex: 1 1 0;
  padding-left: 3em;
  line-height: 30px;
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

@media only print {
  .detail-key,
  .detail-value {
    font-size: 12px !important;
    line-height: 20px !important;
  }
  .crp-details-header {
    font-size: 14px !important;
  }
}
</style>
