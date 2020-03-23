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
        <tr class="cursor-pointer" @click="handleTableRowClick(item)">
          <td class="anchor-text">{{ item["corp_num"] }}</td>
          <td>{{ item["corp_typ_cd"] }}</td>
          <td>{{ item["corp_nme"] }}</td>
          <td>{{ item["recognition_dts"] }}</td>
          <td>{{ item["state_typ_cd"] }}</td>
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
  },
  methods: {
    handleTableRowClick(item) {
      window.open(`/corporation/${item["corp_num"]}`);
    }
  }
};
</script>
