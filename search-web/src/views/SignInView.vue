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
      this.$router.push({
        name: "Home"
      });
      window.location.reload(true);
    },
    syncUserProfile() {}
  }
};
</script>

<style></style>
