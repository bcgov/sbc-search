import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home
  },
  {
    path: "/corpparty/:id",
    name: "corpPartyDetails",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorpPartyDetails.vue")
  },
  {
    path: "/corporation/:id",
    name: "corporationDetails",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorporationDetails.vue")
  },
  {
    path: "/corporation",
    name: "corporation",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorporationSearch.vue")
  }
];

const router = new VueRouter({
  routes
});

export default router;
