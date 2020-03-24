<template>
  <SbcSignin
    :idp-hint="idpHint"
    :redirect-url-login-fail="redirectUrlLoginFail"
    @keycloak-session-ready="updateHeader()"
    @sync-user-profile-ready="syncUserProfile()"
  ></SbcSignin>
</template>

<script>
import SbcSignin from "sbc-common-components/src/components/SbcSignin.vue";
import KeyCloakService from "sbc-common-components/src/services/keycloak.services";
import ApiService from "@/api/ApiService.js";

export default {
  components: {
    SbcSignin
  },
  props: {
    idpHint: {
      default: "bcsc",
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
    async updateHeader() {
      const KEYCLOACK_TOKEN = sessionStorage.getItem("KEYCLOAK_TOKEN");
      if (KEYCLOACK_TOKEN) {
        ApiService.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${KEYCLOACK_TOKEN}`;
      }
      this.$router.push({
        name: "Home"
      });
    },
    syncUserProfile() {}
  }
};
</script>

<style></style>
