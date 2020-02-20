<template>
  <div>
    <h5 class="font-weight-regular body-1 mb-3">
      <i>Other offices held at</i> {{ details.corp_nme }}
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
              <td>
                {{ o.short_desc }}
              </td>
              <td>
                <a
                  :href="`#/details?corp_party_id=${o['corp_party_id']}`"
                  target="blank"
                  >{{ o["corp_party_id"] }}</a
                >
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
      <i>Other</i> {{ details.last_nme }}, {{ details.first_nme }}
      {{ details.middle_nme }} <i>at company</i> {{ details.corp_nme }}
    </h5>
    <div v-if="officesheld.same_name_and_company && officesheld.same_name_and_company.length > 0">
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
            <tr v-for="(o, index) in officesheld.same_name_and_company" :key="index">
              <td>
                {{ o.party_typ_cd }}
              </td>
              <td>
                <a
                  :href="`#/details?corp_party_id=${o['corp_party_id']}`"
                  target="blank"
                  >{{ o["corp_party_id"] }}</a
                >
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
      <i>Other</i> {{ details.last_nme }}, {{ details.first_nme }}
      {{ details.middle_nme }} <i>at address</i> {{ details.addr }}
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
            <tr
              v-for="(o, index) in officesheld.same_addr"
              :key="index"
            >
              <td>
                {{ o.party_typ_cd }}
              </td>
              <td>
                <a
                  :href="`#/details?corp_party_id=${o['corp_party_id']}`"
                  target="blank"
                  >{{ o["corp_party_id"] }}</a
                >
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
</template>

<script>
export default {
  props: {
    officesheld: {
      default: function() {
        return {
          same_addr: null,
          same_name_and_company: null
        };
      },
      type: Object
    },
    details: {
      default: function() {
        return {
          corp_nme: null,
          last_nme: null,
          first_nme: null,
          middle_nme: null,
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

<style lang="sass">
.office-table
    border: 1px solid $COLOR_GREY
    color: $COLOR_GREY
</style>
