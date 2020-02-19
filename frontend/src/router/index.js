import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "home",
    component: Home
  },
  {
    path: "/details",
    name: "details",
    component: () =>
      import(/* webpackChunkName: "results" */ "../views/Details.vue")
  },
  {
    path: "/corporation_details",
    name: "corporation_details",
    component: () =>
      import(
        /* webpackChunkName: "results" */ "../views/CorporationDetails.vue"
      )
  }
];

const router = new VueRouter({
  routes
});

export default router;
