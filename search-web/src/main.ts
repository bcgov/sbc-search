import axios from "axios";
import Vue from "vue";
import App from "./App.vue";
import "./registerServiceWorker";
import router from "./router";
import store from "./store";
import vuetify from "./plugins/vuetify";

Vue.config.productionTip = false;

saveConfigToSessionStorage().then(data => {
  renderVue();
});

async function saveConfigToSessionStorage() {
  const authConfigPath = `${process.env.BASE_URL}config/configuration.json`;
  const authConfig = await axios.get(authConfigPath);
  sessionStorage.setItem("AUTH_API_CONFIG", JSON.stringify(authConfig));
}

function renderVue() {
  new Vue({
    router,
    store,
    vuetify,
    render: h => h(App)
  }).$mount("#app");
}
