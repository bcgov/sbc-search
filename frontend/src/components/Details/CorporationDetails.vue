<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <div class="mb-10 d-flex justify-space-between align-center">
            <h2 class="display-1">
              Corporation Details for Inc. #{{ details.corp_num }}
            </h2>
            <PrintButton></PrintButton>
          </div>
        </v-col>
      </v-row>
      <v-row justify="space-between">
        <v-col cols="6">
          <ul class="pa-0 ma-0 detail-list">
            <li class="d-flex w-100 detail-list-item mb-5">
              <span class="detail-key font-weight-bold">Company Name(s)</span>
              <div class="detail-value">
                <span
                  v-for="(name, index) in details.NAMES"
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
              <div class="d-flex w-100 detail-list-item">
                <span class="detail-key font-weight-bold"
                  >Delivery Address</span
                >
                <span class="detail-value">{{ office.delivery_addr }}</span>
              </div>

              <div class="d-flex w-100 detail-list-item">
                <span class="detail-key font-weight-bold">Mailing Address</span>
                <span class="detail-value">{{ office.mailing_addr }}</span>
              </div>

              <div class="d-flex w-100 detail-list-item">
                <span class="detail-key font-weight-bold">Type</span>
                <span class="detail-value">{{ office.office_typ_cd }}</span>
              </div>

              <div class="d-flex w-100 detail-list-item">
                <span class="detail-key font-weight-bold">Email</span>
                <span class="detail-value">{{ office.email_address }}</span>
              </div>
            </li>
          </ul>
        </v-col>
        <v-col cols="6">
          <CorporationFilings></CorporationFilings>
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
      return pick(this.details, ["corp_num", "state_typ_cd", "admin_email"]);
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
</style>
