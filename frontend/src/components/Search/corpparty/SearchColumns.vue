<template>
  <div>
    <div>
      Show Columns:
      <div
        @click="handleClick('active')"
        class="d-inline-block search-column pl-2 pr-2"
        :class="{ 'search-column-active': initColumn === 'active' }"
      >
        Active/Historical
      </div>
      <div
        @click="handleClick('addr')"
        class="d-inline-block search-column search-column-br pl-2 pr-2"
        :class="{ 'search-column-active': initColumn === 'addr' }"
      >
        Address
      </div>
      <div
        @click="handleClick('none')"
        class="d-inline-block search-column pl-2 pr-2"
        :class="{ 'search-column-active': initColumn === 'none' }"
      >
        None
      </div>
    </div>
    <div class="mb-4 mt-5 ad-info-header cursor-pointer" @click="tips = !tips">
      Additional Information
      <v-icon color="#2f7fd4" class="search-tips-icon" v-if="tips">
        {{ chevronUp }}
      </v-icon>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-else>
        {{ chevronDown }}
      </v-icon>
    </div>
    <div v-if="tips">
      Table data will load faster if you select only of the above, and fastest
      if you select "None"
    </div>
  </div>
</template>

<script>
import { mdiChevronUp, mdiChevronDown } from "@mdi/js";

export default {
  props: {
    initColumn: {
      default: "none",
      type: String
    }
  },
  data() {
    return {
      active: this.initColumn,
      chevronUp: mdiChevronUp,
      chevronDown: mdiChevronDown,
      tips: false
    };
  },
  methods: {
    handleClick(type) {
      this.$emit("click", type);
    }
  }
};
</script>
<style lang="scss">
.search-column {
  line-height: 1 !important;
  cursor: pointer;
}
.search-column-br {
  border-left: 1px solid black;
  border-right: 1px solid black;
}

.search-column-active {
  font-weight: bold;
  text-decoration: underline;
}

.ad-info-header {
  color: #2f7fd4;
  text-decoration: underline;
}
</style>
