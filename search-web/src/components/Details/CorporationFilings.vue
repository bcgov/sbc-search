<template>
  <div>
    <!--
    <h5 class="outline mb-5">Folio Number:</h5>
    <v-text-field
      solo
      class="folio-input"
      placeholder="Enter Folio Number"
    ></v-text-field>
    -->
    <a @click.prevent="handleClick" class="body-2">Link to BC Online</a>
  </div>
</template>

<script>
import { getDeepLink } from "@/util/index.ts";
export default {
  props: {
    corp_num: {
      default: null,
      type: String
    }
  },
  methods: {
    handleClick() {
      window.open(getDeepLink(this.corp_num));
    }
  }
};
</script>

<style lang="scss">
.folio-input {
  width: 215px;
}
.v-application .folio-pay-btn {
  letter-spacing: 0 !important;
  text-transform: none !important;
}
</style>
