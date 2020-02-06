<template>
  <div>
    <SearchFilter
      v-for="(filter, index) in filters"
      :key="index"
      :field="filter.field"
      :operator="filter.operator"
      :value="filter.value"
    ></SearchFilter>
    <AddFilter></AddFilter>
    <div>
      <SbcButton title="Search" @click.native="handleClick"></SbcButton>
    </div>
  </div>
</template>

<script>
import AddFilter from "@/components/Filter/AddFilter.vue";
import SearchFilter from "@/components/Filter/Filter.vue";
import SbcButton from "@/components/SbcButton.vue";
import { mapState } from "vuex";
export default {
  computed: {
    ...mapState(["filters"])
  },
  components: {
    AddFilter,
    SearchFilter,
    SbcButton
  },
  methods: {
    handleClick() {
      let queryString = "";
      let counter = 0;
      this.filters.map(filter => {
        if (counter >= 1) {
          queryString += "&";
        }
        queryString += Object.keys(filter)
          .map(key => key + "=" + filter[key])
          .join("&");
        counter++;
      });

      this.$router.push({
        name: "results",
        query: {
          advanced: true,
          queryString: queryString
        }
      });
    }
  }
};
</script>

<style></style>
