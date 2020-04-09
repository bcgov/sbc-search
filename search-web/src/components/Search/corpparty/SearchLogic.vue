<template>
  <div>
    <v-select
      background-color="#e5e8ec"
      class="search-logic"
      :height="height"
      v-model="select"
      :items="items"
      filled
    ></v-select>
  </div>
</template>

<script>
export default {
  props: {
    height: {
      default: 40,
      type: Number
    },
    logic: {
      default: "Any",
      type: String
    }
  },
  data() {
    return {
      select: this.logic,
      items: [
        {
          text: "All",
          value: "ALL"
        },
        {
          text: "Any",
          value: "ANY"
        }
      ]
    };
  },
  watch: {
    select(nl) {
      this.$emit("update:logic", nl);
    }
  }
};
</script>
<style lang="scss">
.search-logic {
  width: 100px;
}
</style>
