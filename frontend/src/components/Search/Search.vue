<template>
  <v-form class="d-flex">
    <div>
      <v-text-field
        v-model="searchQuery"
        dense
        type="text"
        filled
        :height="59"
        placeholder="Text...."
        :disabled="disabled"
      ></v-text-field>
    </div>
    <div>
      <SbcButton
        type="submit"
        class="ml-2"
        title="Search"
        @click.prevent.native="handleSubmit"
        :disabled="disabled"
      ></SbcButton>
      <SbcButton
        class="ml-2"
        title="Clear"
        :variant="2"
        :disabled="disabled"
      ></SbcButton>
    </div>
  </v-form>
</template>

<script>
import SbcButton from "@/components/SbcButton.vue";
export default {
  props: {
    disabled: {
      default: false,
      type: Boolean
    }
  },
  data() {
    return {
      searchQuery: null
    };
  },
  components: {
    SbcButton
  },
  methods: {
    handleSubmit() {
      if (this.disabled) return;
      this.$router.push({
        query: {
          page: 1,
          searchQuery: this.searchQuery
        }
      });
    }
  }
};
</script>

<style lang="sass"></style>
