<template>
  <div>
    <SearchFilter></SearchFilter>
    <AddFilter></AddFilter>
    <div>
      <router-link :to="{ name: 'results' }">
        <SbcButton title="Search"></SbcButton>
      </router-link>
    </div>
  </div>
</template>

<script>
import AddFilter from "@/components/Filter/AddFilter.vue";
import SearchFilter from "@/components/Filter/Filter.vue";
import SbcButton from "@/components/SbcButton.vue";
export default {
  components: {
    AddFilter,
    SearchFilter,
    SbcButton
  }
};
</script>

<style></style>
