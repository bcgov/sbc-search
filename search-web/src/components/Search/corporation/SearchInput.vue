<template>
  <div>
    <v-text-field
      class="search-input"
      label="Search Term"
      :height="height"
      v-model="searchQuery"
      placeholder="eg. John Smith"
      filled
    />
  </div>
</template>

<script>
export default {
  props: {
    height: {
      default: 40.8,
      type: Number
    },
    props: {
      query: {
        default: null,
        type: String
      }
    }
  },
  data() {
    return {
      searchQuery: this.query
    };
  },
  mounted() {
    this.$root.$on("setCorpSearchInput", r => (this.searchQuery = r));
  },
  methods: {
    clear() {
      this.searchQuery = "";
    }
  },
  watch: {
    searchQuery(nq) {
      this.$emit("update:query", nq);
    }
  }
};
</script>

<style lang="scss">
.search-input {
  width: 400px;
}
</style>
