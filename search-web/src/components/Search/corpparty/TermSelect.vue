<template>
  <v-select
    background-color="#e5e8ec"
    class="term-select"
    filled
    v-model="select"
    :items="items"
    label="Term"
  ></v-select>
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
  data () {
    return {
      select: this.init
    }
  },
  watch: {
    select (ns) {
      this.$emit('change', ns)
      this.$emit('update:selected', ns)
    }
  }
}
</script>

<style></style>
