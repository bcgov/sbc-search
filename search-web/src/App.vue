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
          <v-container>
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
  data() {
    return {
      inAuth: false
    };
  },
  async mounted() {
    sessionStorage.setItem("AUTH_API_CONFIG", JSON.stringify(AuthConfig));
    this.handleJWT();
    await KeyCloakService.setKeycloakConfigUrl(`/config/kc/keycloak.json`);
  },
  methods: {
    handleJWT() {
      const KEYCLOACK_TOKEN = sessionStorage.getItem("KEYCLOAK_TOKEN");
      if (!KEYCLOACK_TOKEN) {
        delete ApiService.defaults.headers.common["Authorization"];
      }
    }
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
