<template>
  <v-text-field
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    placeholder="eg. John Smith"
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
      default: 40.5,
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
        this.$store.commit("filters/setSearchValue", {
          uid: this.uid,
          value: value
        });
      }
    },
    ...mapGetters({
      getFilterValue: "filters/getFilterValue"
    })
  },
  data() {
    return {
      searchIcon: mdiMagnify
    };
  }
};
</script>

<style></style>
