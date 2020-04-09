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
    <div class="mb-4 mt-5 cursor-pointer" @click="tips = !tips">
      <div class="d-inline-block ad-info-header">Additional Information</div>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-if="tips">
        keyboard_arrow_up
      </v-icon>
      <v-icon color="#2f7fd4" class="search-tips-icon" v-else>
        keyboard_arrow_down
      </v-icon>
    </div>
    <div v-if="tips">
      Table data will load faster if you select only of the above, and fastest
      if you select "None"
    </div>
  </div>
</template>

<script>
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
