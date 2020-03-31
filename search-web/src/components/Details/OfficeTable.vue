<template>
  <div>
    <div v-if="!isEmpty(officesheld)">
      <h5 class="font-weight-regular body-1 mb-3">
        <i>Other offices held at</i> {{ details.corpNme }}
      </h5>
      <div v-if="offices && offices.length > 0">
        <v-simple-table class="office-table">
          <template v-slot:default>
            <thead>
              <tr>
                <th>Office Held</th>
                <th>Filing #</th>
                <th>Year</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(o, index) in offices" :key="index">
                <td class="office-held-desc">
                  {{ o.shortDesc }}
                </td>
                <td>
                  <a :href="`/corpparty/${o['corpPartyId']}`" target="blank">
                    {{ o["corpPartyId"] }}
                  </a>
                </td>
                <td>
                  -
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
      <div v-else>
        <h5>No offices found</h5>
      </div>
      <h5 class="font-weight-regular body-1 mb-3 mt-6">
        <i>Other</i> {{ details.lastNme }}, {{ details.firstNme }}
        {{ details.middleNme }} <i>at company</i> {{ details.corpNme }}
      </h5>
      <div
        v-if="
          officesheld.same_name_and_company &&
            officesheld.same_name_and_company.length > 0
        "
      >
        <v-simple-table class="office-table">
          <template v-slot:default>
            <thead>
              <tr>
                <th>Office Held</th>
                <th>Filing #</th>
                <th>Year</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(o, index) in officesheld.same_name_and_company"
                :key="index"
              >
                <td>
                  {{ o.partyTypCd }}
                </td>
                <td>
                  <a :href="`/corpparty/${o['corpPartyId']}`" target="blank">
                    {{ o["corpPartyId"] }}
                  </a>
                </td>
                <td>
                  {{ o.year || "-" }}
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
      <div v-else>
        <h5>None found</h5>
      </div>

      <h5 class="font-weight-regular body-1 mb-3 mt-6">
        <i>Other</i> {{ details.lastNme }}, {{ details.firstNme }}
        {{ details.middleNme }} <i>at address</i> {{ details.addr }}
      </h5>
      <div v-if="officesheld.same_addr && officesheld.same_addr.length > 0">
        <v-simple-table class="office-table">
          <template v-slot:default>
            <thead>
              <tr>
                <th>Office Held</th>
                <th>Filing #</th>
                <th>Year</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(o, index) in officesheld.same_addr" :key="index">
                <td>
                  {{ o.partyTypCd }}
                </td>
                <td>
                  <a :href="`/corpparty/${o['corpPartyId']}`" target="blank">
                    {{ o["corpPartyId"] }}
                  </a>
                </td>
                <td>
                  {{ o.year || "-" }}
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
      </div>
      <div v-else>
        <h5>None found</h5>
      </div>
    </div>
    <div v-else class="d-flex justify-center align-center">
      <v-progress-circular
        :size="70"
        :width="7"
        color="black"
        indeterminate
      ></v-progress-circular>
    </div>
  </div>
</template>

<script>
import isEmpty from "lodash-es/isEmpty";
export default {
  props: {
    officesheld: {
      default: function() {
        return {
          sameAddr: null,
          sameNameAndCompany: null
        };
      },
      type: Object
    },
    details: {
      default: function() {
        return {
          corpNme: null,
          lastNme: null,
          firstNme: null,
          middleNme: null,
          addr: null
        };
      },
      type: Object
    }
  },
  computed: {
    offices() {
      if (this.officesheld && this.officesheld.offices) {
        return this.officesheld.offices;
      } else {
        return null;
      }
    }
  },
  methods: {
    isEmpty
  }
};
</script>

<style lang="scss">
.office-table {
  border: 1px solid $COLOR_GREY;
  color: $COLOR_GREY;
}
</style>
