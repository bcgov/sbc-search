<template>
  <div class="home">
    <h1>Welcome to Director Search</h1>
    <h4 class="mt-3 body-1 mb-10">
      Search for offices held at active and historical BC companies
    </h4>
    <v-form>
      <div v-for="(criteria, index) in filters" :key="index">
        <div v-if="index > 0">
          <SearchCriteria :uid="criteria.uid" :remove="true"></SearchCriteria>
        </div>
        <div v-else>
          <SearchCriteria :uid="criteria.uid"></SearchCriteria>
        </div>
      </div>
      <div class="d-flex justify-space-between">
        <AddFilterButton
          title="Add Filter"
          @click.native.prevent="addFilter"
        ></AddFilterButton>
        <SbcButton
          type="submit"
          title="Search"
          @click.native.prevent="handleSearch"
        ></SbcButton>
      </div>
    </v-form>
    <div class="mt-10">
      <ServerSideTable></ServerSideTable>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import AddFilterButton from "@/components/Filter/AddFilterButton.vue";
import SearchCriteria from "@/components/Search/SearchCriteria.vue";
import { mapGetters } from "vuex";
import { omit, isEmpty } from "lodash-es";
const qs = require("qs");
import { searchApi } from "@/api/SearchApi";
import ServerSideTable from "@/components/Search/ServerSideTable.vue";
import { buildQueryString } from "@/util/index.ts";
export default {
  components: {
    SbcButton,
    SearchCriteria,
    AddFilterButton,
    ServerSideTable
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
  mounted() {
    if (!isEmpty(this.$route.query)) {
      const queryFilters = omit(this.$route.query, "mode");
      if (typeof queryFilters.field === "string") {
        queryFilters.uid = this.uid++;
        this.$store.commit("filters/setFilters", [queryFilters]);
        return;
      }

      if (Array.isArray(queryFilters.field)) {
        let temp = [];
        const length = queryFilters.field.length;
        for (let i = 0; i < length; i++) {
          temp.push({
            uid: this.uid++,
            field: queryFilters.field[i],
            operator: queryFilters.operator[i],
            value: queryFilters.value[i]
          });
        }
        this.$store.commit("filters/setFilters", temp);
      }
    }
  },
  methods: {
    addFilter(field = "first_nme", operator = "exact", value = "") {
      this.uid++;
      this.$store.commit("filters/addFilter", {
        uid: this.uid,
        field,
        operator,
        value
      });
    },
    handleSearch() {
      const queryString = buildQueryString(this.filters);
      this.$router.push({
        query: qs.parse(queryString)
      });
    }
  }
};
</script>
