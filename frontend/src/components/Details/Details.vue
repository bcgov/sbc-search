<template>
  <div>
    <ul>
      <li
        v-for="(val, key) in filteredDetail"
        :key="key"
        class="d-flex w-100 detail-list-item"
      >
        <span class="font-weight-bold mb-1 detail-key">{{ getText(key) }}</span>
        <span class="detail-value">{{ val }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
import { getTextFromValues } from "@/plugins/utils.js";
import { RESULT_HEADERS } from "@/plugins/config.js";
import { omit } from "lodash-es";
import { corpPartySearch } from "@/plugins/SearchApi.js";
import dayjs from "dayjs";
export default {
  computed: {
    filteredDetail() {
      const filtered = omit(this.detail, [
        "postal_cd",
        "province",
        "corp_party_id"
      ]);
      filtered["appointment_dt"] = dayjs(filtered["appointment_dt"]).format(
        "YYYY-MM-DD"
      );
      filtered["cessation_dt"] = dayjs(filtered["cessation_dt"]).format(
        "YYYY-MM-DD"
      );
      filtered[
        "addr_line_1"
      ] = `${filtered["addr_line_1"]}, ${this.detail["postal_cd"]}, ${this.detail["province"]}`;
      return filtered;
    }
  },
  methods: {
    getText(data) {
      return getTextFromValues(RESULT_HEADERS, data);
    }
  },
  data() {
    return {
      detail: {}
    };
  },
  mounted() {
    const corp_party_id = this.$route.query["corp_party_id"];
    if (corp_party_id) {
      corpPartySearch(corp_party_id).then(result => {
        this.detail = result.data;
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
