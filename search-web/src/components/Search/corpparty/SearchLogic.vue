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
      default: 'ANY',
      type: String
    },
    init: {
      default: 'ANY',
      type: String
    }
  },
  data () {
    return {
      select: this.init,
      items: [
        {
          text: 'All',
          value: 'ALL'
        },
        {
          text: 'Any',
          value: 'ANY'
        }
      ]
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.select = this.init
    })
  },
  watch: {
    select (nl) {
      this.$emit('update:logic', nl)
    }
  }
}
</script>
<style lang="scss">
.search-logic {
  width: 100px;
}
</style>
