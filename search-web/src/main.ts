import axios from "axios";
import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";
import { fetchConfig } from "@/util";

Vue.config.productionTip = false;

saveConfigToSessionStorage().then(data => {
  renderVue();
});

async function saveConfigToSessionStorage() {
  await fetchConfig();
}

function renderVue() {
  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
  }).$mount("#app");
}
