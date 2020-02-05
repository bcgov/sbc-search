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
      <SbcButton
        class="ml-2"
        title="Search"
        @click.native="handleSearch"
      ></SbcButton>
      <SbcButton class="ml-2" title="Clear" :variant="2"></SbcButton>
    </div>
  </div>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
import ApiService from "@/plugins/ApiService.js";
export default {
  components: {
    SbcButton
  },
  methods: {
    async handleSearch() {
      const result = await ApiService.get("/person/search", {
        params: {
          page: 1,
          query: "a"
        }
      });
      console.log("Result", result);
    }
  }
};
</script>

<style lang="sass"></style>
