<template>
  <div>
    <v-select
      class="field-select"
      filled
      v-model="select"
      :items="items"
      label="Field"
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
  beforeUpdate() {
    this.select = this.init;
  },
  mounted() {
    this.$nextTick(() => {
      this.select = this.init;
    });
  },
  data() {
    return {
      select: this.init
    };
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
