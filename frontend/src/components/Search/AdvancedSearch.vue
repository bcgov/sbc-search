<template>
  <div>
    <SearchFilter></SearchFilter>
    <AddFilter></AddFilter>
    <div>
      <SbcButton title="Search"></SbcButton>
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
