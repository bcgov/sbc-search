<template>
  <v-app>
    <div class="main-wrapper">
      <div class="content">
        <div class="content-header">
          <SbcHeader
            idpHint="bcros"
            redirect-on-login-success="/"
            redirect-on-login-fail="/"
          >
            <template v-slot:login-button-text>
              Log In
            </template>
          </SbcHeader>
        </div>
        <div class="content-body">
          <router-view />
        </div>
      </div>
      <div class="footer">
        <SbcFooter></SbcFooter>
      </div>
    </div>
  </v-app>
</template>

<script lang="ts">
import Vue from "vue";
import "@bcgov/bc-sans/css/BCSans.css";
import { mapGetters } from "vuex";
import KeyCloakService from "sbc-common-components/src/services/keycloak.services";

import SbcHeader from "sbc-common-components/src/components/SbcHeader.vue";
import SbcFooter from "sbc-common-components/src/components/SbcFooter.vue";
import ApiService from "@/api/ApiService.js";

export default Vue.extend({
  components: {
    SbcHeader,
    SbcFooter
  },
  async mounted() {
    const testConfig = {
      AUTH_URL: "https://dev.bcregistry.ca/cooperatives/auth/",
      VUE_APP_PAY_ROOT_API: "https://pay-api-dev.pathfinder.gov.bc.ca/api/v1",
      VUE_APP_AUTH_ROOT_API: "http://localhost:80/api/v1",
      VUE_APP_LEGAL_ROOT_API:
        "https://legal-api-dev.pathfinder.gov.bc.ca/api/v1",
      VUE_APP_STATUS_ROOT_API:
        "https://status-api-dev.pathfinder.gov.bc.ca/api/v1",
      VUE_APP_PATH_NEW_BUSINESS:
        "https://business-create-dev.pathfinder.gov.bc.ca/businesses/"
    };
    sessionStorage.setItem("AUTH_API_CONFIG", JSON.stringify(testConfig));

    if (sessionStorage.getItem("KEYCLOAK_TOKEN")) {
      ApiService.defaults.headers.common[
        "Authorization"
      ] = `Bearer ${sessionStorage.getItem("KEYCLOAK_TOKEN")}`;
    }
    await KeyCloakService.setKeycloakConfigUrl(`/config/kc/keycloak.json`);
  }
});
</script>

<style lang="scss">
* {
  font-family: "BCSans", "Verdana", "Arial", "sans-serif" !important;
}
.material-icons {
  font-family: "Material Icons" !important;
}
.layout-wrapper {
  background-color: #f1f3f6;
}
.app-body {
  margin-top: 0 !important;
}
.cursor-pointer {
  cursor: pointer;
}

.export-btn {
  letter-spacing: 0 !important;
  text-transform: none !important;
  padding: 0 2em !important;
}

.anchor-text {
  text-decoration: underline;
  color: #2076d2;
}

.color-gray {
  color: $COLOR_GREY;
}

.main-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
  background-color: #f1f3f6;
}
.content-body {
  max-width: 1500px;
  margin: 0 auto;
  padding: 2em 0;
}
html,
body {
  height: 100%;
}
.content {
  flex: 1 0 auto;
}
.footer {
  flex-shrink: 0;
}

@media (max-width: 1600px) {
  .content-body {
    padding: 2em;
  }
}
</style>
