import Vue from 'vue'
import App from './App.vue'
import './registerServiceWorker'
import Hotjar from 'vue-hotjar'
import { getVueRouter } from '@/router'
import store from './store'
import vuetify from './plugins/vuetify'
import ConfigHelper from '@/util/config-helper'
import KeyCloakService from 'sbc-common-components/src/services/keycloak.services'

Vue.config.productionTip = false

// Setup Hotjar
Vue.use(Hotjar, {
  id: `${process.env.HOTJAR_ID}`,
  isProduction: true,
  snippetVersion: 6
})

// main code
async function start () {
  // fetch config from environment and API
  // must come first as inits below depend on config
  await ConfigHelper.fetchConfig()

  console.info('Starting Keycloak service...') // eslint-disable-line no-console
  let random = new Date().toISOString().substring(0, 10)
  await KeyCloakService.setKeycloakConfigUrl(
    `${process.env.VUE_APP_PATH}config/kc/keycloak.json?${random}`
  )

  // start Vue application
  console.info('Starting app...') // eslint-disable-line no-console
  new Vue({
    router: getVueRouter(),
    store,
    vuetify,
    render: h => h(App)
  }).$mount('#app')
}

// execution and error handling
start().catch(error => {
  console.error(error) // eslint-disable-line no-console
})
