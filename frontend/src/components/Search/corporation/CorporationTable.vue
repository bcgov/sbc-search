<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="corporations"
      :footer-props="{
        'items-per-page-options': [20]
      }"
    >
      <template v-slot:item="{ item }">
        <tr>
          <td>{{ item["inc"] }}</td>
          <td>{{ item["corp_nme"] }}</td>
          <td>{{ item["inc_date"] }}</td>
          <td>{{ item["status"] }}</td>
          <td>{{ item["addr"] }}</td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script>
import { CORPORATION_HEADERS } from "@/config/index.ts";

export default {
  props: {
    corporations: {
      default: null,
      type: Array
    }
  },
  data() {
    return {
      headers: CORPORATION_HEADERS
    };
  }
};
</script>

<style></style>
