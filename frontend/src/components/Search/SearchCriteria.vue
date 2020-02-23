<template>
  <div>
    <SearchSelect></SearchSelect>
    <SearchInput :query.sync="searchQuery" class="mt-10"></SearchInput>
  </div>
</template>

<script>
import SearchSelect from "@/components/Search/SearchSelect.vue";
import SearchInput from "@/components/Search/SearchInput.vue";

export default {
  components: {
    SearchInput,
    SearchSelect
  },
  data() {
    return {
      searchQuery: null
    };
  }
};
</script>

<style></style>
