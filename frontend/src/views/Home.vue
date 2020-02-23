<template>
  <div class="home">
    <h1>Welcome to Director Search</h1>
    <h4 class="mt-3 body-1 mb-10">Search for offices held at active and historical BC companies</h4>
    <div v-for="(criteria, index) in filters" :key="index">
      <div v-if="index > 0">
        <SearchCriteria :uid="criteria.uid" :remove="true"></SearchCriteria>
      </div>
      <div v-else>
        <SearchCriteria :uid="criteria.uid"></SearchCriteria>
      </div>
    </div>

    <div class="d-flex justify-space-between">
      <AddFilterButton title="Add Filter" @click.native.prevent="addFilter"></AddFilterButton>
      <SbcButton title="Search"></SbcButton>
    </div>
    {{ filters }}
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import AddFilterButton from "@/components/Filter/AddFilterButton.vue";
import SearchCriteria from "@/components/Search/SearchCriteria.vue";
import { mapGetters } from "vuex";
export default {
  components: {
    SbcButton,
    SearchCriteria,
    AddFilterButton
  },
  computed: {
    ...mapGetters({
      filters: "filters/getFilters",
      numFilters: "filters/getNumFilters"
    })
  },
  data() {
    return {
      uid: 0,
      searchQuery: null
    };
  },
  methods: {
    addFilter() {
      this.uid++;
      this.$store.commit("filters/addFilter", {
        uid: this.uid,
        field: "first_nme",
        operator: "exact",
        query: ""
      });
    }
  }
};
</script>
