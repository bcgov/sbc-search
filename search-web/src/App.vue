<template>
  <v-app>
    <Snackbar></Snackbar>
    <div v-if="$vuetify.breakpoint.smAndDown">
      <BackToTop bottom="10px" right="10px" visibleoffset="600">
        <v-btn class="mx-2" fab dark small color="primary">
          <v-icon dark>expand_less</v-icon>
        </v-btn>
      </BackToTop>
    </div>
    <div v-else>
      <BackToTop bottom="20px" right="20px" visibleoffset="600">
        <v-btn class="mx-2" fab dark color="primary">
          <v-icon dark>expand_less</v-icon>
        </v-btn>
      </BackToTop>
    </div>

    <div class="main-wrapper">
      <div class="content">
        <div class="content-header">
          <SbcHeader idpHint="bcros">
            <template v-slot:login-button-text>Log In</template>
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
import BackToTop from "vue-backtotop";
import SbcHeader from "sbc-common-components/src/components/SbcHeader.vue";
import SbcFooter from "sbc-common-components/src/components/SbcFooter.vue";
import TokenService from "sbc-common-components/src/services/token.services";
import Snackbar from "@/components/Snackbar.vue";
const tokenService = new TokenService();

export default Vue.extend({
  components: {
    SbcHeader,
    SbcFooter,
    BackToTop,
    Snackbar
  },

  async mounted() {
    try {
      await KeyCloakService.setKeycloakConfigUrl(
        `${process.env.BASE_URL}config/kc/keycloak.json`
      );

      const KEYCLOACK_TOKEN = sessionStorage.getItem("KEYCLOAK_TOKEN");
      if (KEYCLOACK_TOKEN) {
        await tokenService.init();
        tokenService.scheduleRefreshTimer();
      }
    } catch (e) {
      console.error(e);
    }
  },
  methods: {}
});
</script>

<style lang="scss">
.letter-spacing-none {
  letter-spacing: 0 !important;
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
  background-color: white !important;
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

.color-dark-grey {
  color: $COLOR_DARK_GREY !important;
}

.color-black {
  color: black;
}

.border-gray {
  border: 1px solid $BORDER_GREY !important;
}

.theme--light.v-text-field > .v-input__control > .v-input__slot:before {
  border-color: $BORDER_GREY !important;
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
