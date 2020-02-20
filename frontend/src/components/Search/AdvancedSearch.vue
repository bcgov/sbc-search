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
      default: "ANY",
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
      modes: ["ANY", "AND"]
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

      if (this.mode === "AND") {
        queryString += "&mode=ALL";
      } else if (this.mode === "ANY") {
        queryString += "&mode=ANY";
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
