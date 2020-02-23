<template>
  <div class="home">
    <h1>Welcome to Director Search</h1>
    <h4 class="mt-3 body-1">
      Search for offices held at active and historical BC companies
    </h4>

    <SearchCriteria></SearchCriteria>
    <div class="d-flex justify-end">
      <SbcButton title="Search"></SbcButton>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import SearchCriteria from "@/components/Search/SearchCriteria.vue";
export default {
  components: {
    SbcButton,
    SearchCriteria
  },

  data() {
    return {
      searchQuery: null
    };
  }
};
</script>
