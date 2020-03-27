<template>
  <v-app>
    <div class="main-wrapper">
      <div class="content">
        <div class="content-header">
          <SbcHeader idpHint="bcros">
            <template v-slot:login-button-text>
              Log In
            </template>
          </SbcHeader>
        </div>
        <div class="content-body">
          <v-container :fluid="$vuetify.breakpoint.mdOnly">
            <router-view />
          </v-container>
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
import AuthConfig from "@/config/authconfig.json";

export default Vue.extend({
  components: {
    SbcHeader,
    SbcFooter
  },
  async mounted() {
    sessionStorage.setItem("AUTH_API_CONFIG", JSON.stringify(AuthConfig));
    await KeyCloakService.setKeycloakConfigUrl(`/config/kc/keycloak.json`);
  },
  methods: {}
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

.content-body {
  margin-top: 2em;
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
.w-100 {
  width: 100% !important;
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

@media (max-width: 600px) {
  .content-body {
    padding: 0em 0.5em;
    margin: 0;
  }
}
</style>
