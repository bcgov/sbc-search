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
        const filter = this.filters.find(f => f.uid === this.uid);
        return filter && filter.query;
      },
      set(value) {
        this.$store.commit("filters/setSearchQuery", {
          uid: this.uid,
          query: value
        });
      }
    },
    ...mapGetters({
      filters: "filters/getFilters"
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
