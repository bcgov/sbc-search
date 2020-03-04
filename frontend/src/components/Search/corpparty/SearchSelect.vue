<template>
  <div>
    <v-select
      class="search-select"
      :label="selectLabel"
      :height="height"
      v-model="select"
      :items="items"
      filled
    ></v-select>
  </div>
</template>

<script>
import { mapGetters } from "vuex";
export default {
  props: {
    items: {
      default: null,
      type: Array
    },
    label: {
      default: null,
      type: String
    },
    initValue: {
      default: null,
      type: String
    },
    height: {
      default: 40,
      type: Number
    },
    selectLabel: {
      default: "Standard",
      type: String
    },
    uid: {
      default: null,
      type: Number
    },
    type: {
      default: "field",
      type: String
    },
    property: {
      default: null,
      type: String
    }
  },
  computed: {
    select: {
      get() {
        console.log(this.uid);
        return this.getFilterProperty(this.uid, this.property);
      },
      set(value) {
        this.$store.commit("corpParty/filters/setSearchPropValue", {
          uid: this.uid,
          property: this.property,
          value: value
        });
      }
    },
    ...mapGetters({
      getFilterProperty: "corpParty/filters/getProperty"
    })
  }
};
</script>

<style lang="scss">
.search-select {
  width: 200px;
}
</style>
