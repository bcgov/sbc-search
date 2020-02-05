<template>
  <div>
    <ul>
      <li
        v-for="(val, key) in detail"
        :key="key"
        class="d-flex w-100 detail-list-item"
      >
        <span class="font-weight-bold mb-1 detail-key">{{ key }}</span>
        <span class="detail-value">{{ val }}</span>
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  data() {
    return {
      detail: {
        Type: "BC",
        Number: "0638995",
        "Company Name": "Dennis Black Consuling Ltd.",
        Status: "Historical",
        Surname: "Black",
        "First Name": "Barbara",
        "Middle Name": "Mary",
        Appointed: "2018-06-7",
        Ceased: "-",
        Address:
          "Site 227, Comp 40, R.R #2 6299 Cherry Creek Road Port Alberni, B.C. V9Y7L6"
      }
    };
  }
};
</script>

<style lang="sass">
.detail-list-item span
    flex: 1 1 0

.detail-value
    color: $COLOR_SECONDARY
.detail-list-item span::first-of-type
    border-right: 1px solid black
</style>
