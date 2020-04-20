<template>
  <div class="corp-op-select-container">
    <v-select
      background-color="#e5e8ec"
      filled
      v-model="select"
      :items="items"
      label="Corporation Type"
      placeholder="Corporation Name or Number"
    ></v-select>
  </div>
</template>

<script>
export default {
  props: {
    initOperator: {
      default: "corpNme",
      type: String
    }
  },
  data() {
    return {
      select: this.initOperator,
      items: [
        {
          text: "Name",
          value: "corpNme"
        },
        {
          text: "Number",
          value: "corpNum"
        }
      ]
    };
  },
  mounted() {
    this.$nextTick(function() {
      this.select = this.initOperator;
    });
  }
};
</script>

<style lang="scss">
.corp-op-select-container {
  max-width: 150px;
}
</style>
