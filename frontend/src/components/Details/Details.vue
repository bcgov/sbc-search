<template>
  <div>
    <ul>
      <li
        v-for="(val, key) in detail"
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
export default {
  methods: {
    getText(data) {
      return getTextFromValues(RESULT_HEADERS, data);
    }
  },
  data() {
    return {
      detail: this.$route.query
    };
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
