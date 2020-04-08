<template>
  <v-text-field
    background-color="#e5e8ec"
    class="search-input"
    label="Search Term"
    :height="height"
    v-model="searchQuery"
    :placeholder="getPlaceHolder()"
    filled
  >
    <template v-slot:append>
      <v-icon>search</v-icon>
    </template>
  </v-text-field>
</template>

<script>
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
      placeholder: "Enter term here..."
    };
  },
  methods: {
    getPlaceHolder() {
      switch (this.selectField) {
        case "anyNme":
          return "James";

        case "firstNme":
          return "John";

        case "lastNme":
          return "Smith";

        case "middleNme":
          return "Allan";

        case "addrLine1":
          return "45 Sesame";

        case "postalCd":
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
