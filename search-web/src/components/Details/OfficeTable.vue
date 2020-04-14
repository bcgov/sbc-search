<template>
  <div>
    <h5 class="font-weight-regular body-1 mb-3">
      <span>Other offices held at</span> {{ details.corpNme }}
    </h5>
    <div>
      <v-simple-table class="office-table">
        <template v-slot:default>
          <thead>
            <tr>
              <th>Office Held</th>
              <th>Filing #</th>
              <th>Year</th>
            </tr>
          </thead>
          <tbody v-if="offices && offices.length > 0">
            <tr v-for="(o, index) in offices" :key="index">
              <td class="office-held-desc">
                {{ o.shortDesc || "-" }}
              </td>
              <td>
                <a :href="`/corpparty/${o['corpPartyId']}`" target="blank">
                  {{ o["corpPartyId"] || "-" }}
                </a>
              </td>
              <td>
                -
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td>-</td>
              <td>-</td>
              <td>-</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>

    <h5 class="font-weight-regular body-1 mb-3 mt-6">
      <span>Other</span> {{ details.lastNme }}, {{ details.firstNme }}
      {{ details.middleNme }} <span>at company</span> {{ details.corpNme }}
    </h5>
    <div>
      <v-simple-table class="office-table">
        <template v-slot:default>
          <thead>
            <tr>
              <th>Office Held</th>
              <th>Filing #</th>
              <th>Year</th>
            </tr>
          </thead>

          <tbody v-if="officesheld.sameNameAndCompany.length > 0">
            <tr
              v-for="(o, index) in officesheld.sameNameAndCompany"
              :key="index"
            >
              <td>
                {{ o.partyTypCd || "-" }}
              </td>
              <td>
                <a :href="`/corpparty/${o['corpPartyId']}`" target="blank">
                  {{ o["corpPartyId"] || "-" }}
                </a>
              </td>
              <td>
                {{ o.year || "-" }}
              </td>
            </tr>
          </tbody>
          <tbody v-else>
            <tr>
              <td>-</td>
              <td>-</td>
              <td>-</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>
    <h5 class="font-weight-regular body-1 mb-3 mt-6">
      <span>Other</span> {{ details.lastNme }}, {{ details.firstNme }}
      {{ details.middleNme }} <span>at address</span> {{ details.addr }}
    </h5>
    <div>
      <v-simple-table class="office-table">
        <template v-slot:default>
          <thead>
            <tr>
              <th>Office Held</th>
              <th>Filing #</th>
              <th>Year</th>
            </tr>
          </thead>
          <tbody v-if="officesheld.sameAddr && officesheld.sameAddr.length > 0">
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
          <tbody v-else>
            <tr>
              <td>-</td>
              <td>-</td>
              <td>-</td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </div>
  </div>
</template>

<script>
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
  }
};
</script>

<style lang="scss">
.office-table {
  border: 1px solid $COLOR_GREY;
  color: $COLOR_GREY;
  max-width: 640px;
}
</style>
