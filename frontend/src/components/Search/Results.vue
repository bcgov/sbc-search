<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="items"
      :items-per-page="10"
      class="elevation-1 result-table"
      @click:row="handleClick"
    ></v-data-table>
  </div>
</template>

<script>
export default {
  methods: {
    handleClick(e) {
      console.log("Clicked", e);
    }
  },
  data() {
    return {
      items: [
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        },
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        },
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        },
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        },
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        },
        {
          surname: "Black",
          middlename: "Mary",
          firstname: "Barbara",
          appointed: "2019-30-31",
          ceased: null,
          acchistory: "Active",
          org: "0559302",
          companyname: "The Word Garden",
          companyaddress: "#123 Sesame St..."
        }
      ],
      headers: [
        {
          text: "Surname",
          value: "surname",
          sortable: true,
          align: "left"
        },
        {
          text: "Middle Name",
          value: "middlename",
          sortable: true,
          align: "left"
        },
        {
          text: "First Name",
          value: "firstname",
          sortable: false,
          align: "left"
        },
        {
          text: "Appointed",
          value: "appointed",
          sortable: false,
          align: "left"
        },
        {
          text: "Ceased",
          value: "ceased",
          sortable: false,
          align: "left"
        },
        {
          text: "Act/Hist",
          value: "acchistory",
          sortable: false,
          align: "left"
        },
        {
          text: "Inc/Org #",
          value: "org",
          sortable: false,
          align: "left"
        },
        {
          text: "Company Name",
          value: "companyname",
          sortable: false,
          align: "left"
        },
        {
          text: "Company Address",
          value: "companyaddress",
          sortable: false,
          align: "left"
        }
      ]
    };
  }
};
</script>

<style lang="sass">
.result-table tbody tr td:first-of-type
  text-decoration: underline
  color: #2a7cd4
  cursor: pointer
</style>
