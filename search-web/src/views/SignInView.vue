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
    updateHeader() {
      console.log("Update Header");
    },
    syncUserProfile() {
      console.log("Sync");
    }
  }
};
</script>

<style></style>
