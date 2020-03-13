<template>
  <div>
    <h5 class="outline mb-5">Folio Number:</h5>
    <v-text-field
      solo
      class="folio-input"
      placeholder="Enter Folio Number"
    ></v-text-field>
    <v-btn height="50" color="primary" class="folio-pay-btn"
      >Pay to See Corporate Filings</v-btn
    >
  </div>
</template>

<script>
export default {};
</script>

<style lang="scss">
.folio-input {
  width: 215px;
}
.v-application .folio-pay-btn {
  letter-spacing: 0 !important;
  text-transform: none !important;
  width: 215px;
}
</style>
