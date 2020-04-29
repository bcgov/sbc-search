<template>
  <SbcSignin
    :idp-hint="idpHint"
    :redirect-url-login-fail="redirectUrlLoginFail"
    @sync-user-profile-ready="syncUserProfile()"
  ></SbcSignin>
</template>

<script>
import SbcSignin from "sbc-common-components/src/components/SbcSignin.vue";
import KeyCloakService from "sbc-common-components/src/services/keycloak.services";
import ApiService from "@/api/ApiService.js";
import TokenService from "sbc-common-components/src/services/token.services";
const tokenService = new TokenService();

export default {
  components: {
    SbcSignin
  },
  props: {
    idpHint: {
      default: "bcros",
      type: String
    },
    redirectUrlLoginFail: {
      default: "",
      type: String
    },
    redirectUrl: {
      default: "",
      type: String
    }
  },
  methods: {
    async syncUserProfile() {
      const KEYCLOACK_TOKEN = sessionStorage.getItem("KEYCLOAK_TOKEN");
      if (KEYCLOACK_TOKEN) {
        ApiService.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${KEYCLOACK_TOKEN}`;
        await tokenService.init();
        tokenService.scheduleRefreshTimer();
      }
      const query = Object.assign({}, this.$route.query);
      const path = this.$route.params.redirectUrl;
      this.$router.push({
        path,
        query
      });
    }
  }
};
</script>

<style></style>
