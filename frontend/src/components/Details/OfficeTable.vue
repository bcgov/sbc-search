<template>
  <div>
    <h5 class="font-weight-regular body-1 mb-3">{{ title }}</h5>
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
          <tr>
            <td>Secretary</td>
            <td>2018</td>
            <td>Site 227, Comp 40, R.R. #2...</td>
          </tr>
          <tr>
            <td>Secretary</td>
            <td>2018</td>
            <td>Site 227, Comp 40, R.R. #2...</td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </div>
</template>

<script>
export default {
  props: {
    title: {
      default: "",
      type: String
    }
  }
};
</script>

<style lang="sass">
.office-table
    border: 1px solid $COLOR_GREY
    color: $COLOR_GREY
</style>
