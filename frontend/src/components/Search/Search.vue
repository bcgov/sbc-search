<template>
  <div class="d-flex">
    <div>
      <v-text-field
        dense
        type="text"
        filled
        :height="59"
        placeholder="Text...."
      ></v-text-field>
    </div>
    <div>
      <SbcButton class="ml-2" title="Search"></SbcButton>
      <SbcButton class="ml-2" title="Clear" :variant="2"></SbcButton>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
export default {
  components: {
    SbcButton
  }
};
</script>

<style lang="sass"></style>
