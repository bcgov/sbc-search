<template>
  <div>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h2 class="display-1">Corporation Details for Inc. #{{ details.corp_num}}</h2>
        </v-col>
      </v-row>
      <v-row justify="space-between">
        <v-col cols="6">
          <ul class="pa-0 ma-0">
            <li
              v-for="(val, key) in filteredDetail"
              :key="key"
              class="d-flex w-100 detail-list-item"
            >
              <span class="detail-key">{{ key }}</span>
              <span class="detail-value">{{ val }}</span>
            </li>
          </ul>
        </v-col>
        <v-col cols="6"></v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
export default {
  props: {
    details: {
      default: null,
      type: Object
    }
  }
};
</script>
<style lang="scss">
</style>