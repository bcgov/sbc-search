<template>
  <div>
    <v-text-field
      v-model="searchQuery"
      placeholder="Search for a director here"
    >
      <template v-slot:append>
        <v-icon>{{ searchIcon }}</v-icon>
      </template>
    </v-text-field>
  </div>
</template>

<script>
import { mdiMagnify } from "@mdi/js";
export default {
  props: {
    query: {
      default: "",
      type: String
    }
  },
  data() {
    return {
      searchQuery: this.query,
      searchIcon: mdiMagnify
    };
  },

  watch: {
    searchQuery(nq) {
      this.$emit("update:query", nq);
    }
  }
};
</script>

<style></style>
