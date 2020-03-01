<template>
  <v-text-field
    class="search-input"
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    placeholder="eg. John Smith"
    filled
  >
    <template v-slot:append>
      <v-icon>{{ searchIcon }}</v-icon>
    </template>
  </v-text-field>
</template>

<script>
import { mdiMagnify } from "@mdi/js";
import { mapGetters } from "vuex";
export default {
  props: {
    query: {
      default: "",
      type: String
    },
    height: {
      default: 40.8,
      type: Number
    },
    uid: {
      default: null,
      type: Number
    }
  },
  computed: {
    searchQuery: {
      get() {
        return this.getFilterValue(this.uid);
      },
      set(value) {
        this.$store.commit("corpParty/filters/setSearchValue", {
          uid: this.uid,
          value: value
        });
      }
    },
    ...mapGetters({
      getFilterValue: "corpParty/filters/getFilterValue"
    })
  },
  data() {
    return {
      searchIcon: mdiMagnify
    };
  }
};
</script>

<style lang="scss">
.search-input {
  width: 268px;
}
</style>
