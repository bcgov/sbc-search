<template>
  <div>
    <SearchFilter
      v-for="(filter, index) in filters"
      :key="index"
      :field="filter.field"
      :operator="filter.operator"
      :value="filter.value"
    ></SearchFilter>
    <AddFilter></AddFilter>
    <div>
      <v-select
        v-if="modeActive"
        v-model="mode"
        :items="modes"
        :placeholder="imode"
        filled
        dense
        height="59"
        class="filter-input d-inline-block mr-5 mode-input"
      ></v-select>
      <SbcButton title="Search" @click.native="handleClick"></SbcButton>
    </div>
  </div>
</template>

<script>
import AddFilter from "@/components/Filter/AddFilter.vue";
import SearchFilter from "@/components/Filter/Filter.vue";
import SbcButton from "@/components/SbcButton.vue";
import { mapState } from "vuex";
export default {
  props: {
    imode: {
      default: "Any",
      type: String
    }
  },
  computed: {
    ...mapState(["filters"]),
    modeActive() {
      return this.filters.length > 1;
    }
  },
  components: {
    AddFilter,
    SearchFilter,
    SbcButton
  },
  data() {
    return {
      mode: this.imode,
      modes: ["Any", "And"]
    };
  },
  methods: {
    handleClick() {
      let queryString = "";
      let counter = 0;
      this.filters.map(filter => {
        if (counter >= 1) {
          queryString += "&";
        }
        queryString += Object.keys(filter)
          .map(key => key + "=" + filter[key])
          .join("&");
        counter++;
      });

      if (this.mode === "And") {
        queryString += "&mode=All";
      } else if (this.mode === "Any") {
        queryString += "&mode=Any";
      }

      this.$router.push({
        query: {
          advanced: true,
          queryString: queryString
        }
      });
    }
  }
};
</script>

<style lang="sass">
.mode-input
  max-width: 125px
</style>
