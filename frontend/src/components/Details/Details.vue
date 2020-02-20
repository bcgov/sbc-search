<template>
  <div>
    <h2 class="headline text-center mb-10">
      Details for Filing #{{ detail.corp_party_id }}
    </h2>
    <v-container>
      <v-row>
        <v-col cols="6">
          <ul>
            <li
              v-for="(val, key) in filteredDetail"
              :key="key"
              class="d-flex w-100 detail-list-item"
            >
              <span class="font-weight-bold mb-1 detail-key">{{
                getText(key)
              }}</span>
              <span class="detail-value">{{ val }}</span>
            </li>
          </ul>
        </v-col>
        <v-col cols="6">
          <OfficeTable
            class="mt-4"
            :details="filteredDetail"
            :officesheld="officesheld"
          ></OfficeTable>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import { getTextFromValues } from "@/plugins/utils.js";
import { RESULT_HEADERS } from "@/plugins/config.js";
import { omit, pick } from "lodash-es";
import { corpPartySearch, corpPartyOfficeSearch } from "@/plugins/SearchApi.js";
import dayjs from "dayjs";
import OfficeTable from "@/components/Details/OfficeTable.vue";

export default {
  components: {
    OfficeTable
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
        "corp_addr"
      ]);
    }
  },
  methods: {
    getText(data) {
      return getTextFromValues(RESULT_HEADERS, data);
    }
  },
  data() {
    return {
      detail: {},
      officesheld: {}
    };
  },
  mounted() {
    const corp_party_id = this.$route.query["corp_party_id"];
    if (corp_party_id) {
      corpPartySearch(corp_party_id).then(result => {
        this.detail = result.data;
      });

      corpPartyOfficeSearch(corp_party_id)
        .then(result => {
          this.officesheld = result.data;
        })
        .catch(() => {
          this.officesheld = {};
        });
    }
  }
};
</script>

<style lang="sass">
.detail-list-item span
    flex: 1 1 0

.detail-value
    color: $COLOR_SECONDARY
.detail-list-item span::first-of-type
    border-right: 1px solid black
</style>
