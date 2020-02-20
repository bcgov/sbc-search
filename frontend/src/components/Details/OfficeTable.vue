<template>
  <div>
    <v-simple-table class="office-table">
      <template v-slot:default>
        <thead>
          <tr>
            <th>Office Held</th>
            <th>Year</th>
            <th>Address</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(o, index) in offices" :key="index">
            <td>
              {{ o.short_desc }}
            </td>
            <td>
              {{ o["year"] }}
            </td>
            <td>{{ o["addr_line_1"] }}</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
import dayjs from "dayjs";

export default {
  props: {
    officesheld: {
      default: null,
      type: Object
    }
  },
  computed: {
    offices() {
      if (this.officesheld && this.officesheld.offices) {
        return this.officesheld.offices.map(o => {
          o.year = dayjs(o["appointment_dt"]).format("YYYY");
          return o;
        });
      } else {
        return null;
      }
    }
  }
};
</script>

<style lang="sass">
.office-table
    border: 1px solid $COLOR_GREY
    color: $COLOR_GREY
</style>
