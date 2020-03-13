import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    meta: {
      title: "Director Search"
    }
  },
  {
    path: "/corpparty/:id",
    name: "corpPartyDetails",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorpPartyDetails.vue"),
    meta: {
      title: route => `Details for Filing #${route.params.id}`
    }
  },
  {
    path: "/corporation/:id",
    name: "corporationDetails",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorporationDetails.vue"),
    meta: {
      title: route => `Corporation Details for Inc. #${route.params.id}`
    }
  },
  {
    path: "/corporation",
    name: "corporation",
    component: () =>
      import(/* webpackChunkName: "about" */ "../views/CorporationSearch.vue"),
    meta: {
      title: "Corporation Search"
    }
  }
];

const router = new VueRouter({
  routes
});

router.beforeEach((to, from, next) => {
  const { title } = to.meta;
  document.title = typeof title === "function" ? title(to) : title;
  next();
});

export default router;
