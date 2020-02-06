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
      <router-link
        :to="{
          name: 'results',
          query: {
            advanced: true
          }
        }"
      >
        <SbcButton title="Search"></SbcButton>
      </router-link>
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
  }
};
</script>

<style></style>
