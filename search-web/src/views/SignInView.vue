<template>
  <SbcSignin
    :idp-hint="idpHint"
    :redirect-url-login-fail="redirectUrlLoginFail"
    @sync-user-profile-ready="syncUserProfile()"
  ></SbcSignin>
</template>

<script>
import SbcSignin from 'sbc-common-components/src/components/SbcSignin.vue'
import KeyCloakService from 'sbc-common-components/src/services/keycloak.services'
import axios from '@/util/axios-auth'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'

export default {
  components: {
    SbcSignin
  },
  props: {
    idpHint: {
      default: 'bcros',
      type: String
    },
    redirectUrlLoginFail: {
      default: '',
      type: String
    },
    redirectUrl: {
      default: '',
      type: String
    }
  },
  methods: {
    async syncUserProfile () {
      const KEYCLOACK_TOKEN = sessionStorage.getItem(SessionStorageKeys.KeyCloakToken)
      axios.defaults.headers.common['Authorization'] = `Bearer ${KEYCLOACK_TOKEN}`
      await KeyCloakService.initializeToken()

      const CURRENT_ACCOUNT = sessionStorage.getItem(SessionStorageKeys.CurrentAccount)
      const CURRENT_ACCOUNT_ID = CURRENT_ACCOUNT
        ? JSON.parse(CURRENT_ACCOUNT).id
        : ''
      axios.defaults.headers['X-Account-Id'] = CURRENT_ACCOUNT_ID

      // const query = Object.assign({}, this.$route.query)
      // const path = this.$route.params.redirectUrl
      // console.log(path)
      this.$router.push('/')
    }
  }
}
</script>

<style></style>
