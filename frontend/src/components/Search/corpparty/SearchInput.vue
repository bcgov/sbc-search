<template>
  <v-text-field
    class="search-input"
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    :placeholder="getPlaceHolder()"
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
    selectField() {
      return this.getFilterProperty(this.uid, "field");
    },
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
      getFilterValue: "corpParty/filters/getFilterValue",
      getFilterProperty: "corpParty/filters/getProperty"
    })
  },
  data() {
    return {
      searchIcon: mdiMagnify,
      placeholder: "Enter term here..."
    };
  },
  methods: {
    getPlaceHolder() {
      switch (this.selectField) {
        case "any_nme":
          return "James";

        case "first_nme":
          return "John";

        case "last_nme":
          return "Smith";

        case "middle_nme":
          return "Allan";

        case "addr_line_1":
          return "45 Sesame";

        case "postal_code":
          return "A1A 1A1";
      }
    }
  }
};
</script>

<style lang="scss">
.search-input {
  width: 268px;
}
</style>
