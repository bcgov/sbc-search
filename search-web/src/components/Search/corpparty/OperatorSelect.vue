<template>
  <div>
    <v-select
      background-color="#e5e8ec"
      filled
      class="operator-select"
      v-model="select"
      :items="items"
      label="Operator"
    ></v-select>
  </div>
</template>

<script>
export default {
  props: {
    items: {
      default: null,
      type: Array
    },
    init: {
      default: null,
      type: String
    }
  },
  data() {
    return {
      select: this.init
    };
  },
  beforeUpdate() {
    this.select = this.init;
  },
  mounted() {
    this.$nextTick(() => {
      this.select = this.init;
    });
  },
  watch: {
    select(ns) {
      this.$emit("change", ns);
      this.$emit("update:selected", ns);
    }
  }
};
</script>

<style></style>
