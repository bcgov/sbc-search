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
export default {
  computed: {
    filteredDetail() {
      const filtered = omit(this.detail, [
        "POSTAL_CD",
        "PROVINCE",
        "CORP_PARTY_ID"
      ]);
      filtered[
        "ADDR_LINE_1"
      ] = `${filtered["ADDR_LINE_1"]}, ${this.detail["POSTAL_CD"]}, ${this.detail["PROVINCE"]}`;
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
    const CORP_PARTY_ID = this.$route.query["CORP_PARTY_ID"];
    if (CORP_PARTY_ID) {
      corpPartySearch(CORP_PARTY_ID).then(result => {
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
