import Vue from "vue";
import VueRouter from "vue-router";
import CorpPartySearch from "../views/CorpPartySearch.vue";
import ApiService from "@/api/ApiService";
import NotFound from "@/views/NotFound.vue";

Vue.use(VueRouter);

const routes = [
  {
    path: "/signin/:idpHint",
    name: "signin",
    component: () =>
      import(/* webpackChunkName: "signin" */ "../views/SignInView.vue"),
    props: true,
    meta: { requiresAuth: false, title: "Sign In" }
  },
  {
    path: "/signin/:idpHint/:redirectUrl",
    name: "signin-redirect",
    component: () =>
      import(/* webpackChunkName: "signin" */ "../views/SignInView.vue"),
    props: true,
    meta: { requiresAuth: false, title: "Sign In" }
  },
  {
    path: "/signin/:idpHint/:redirectUrl/:redirectUrlLoginFail",
    name: "signin-redirect-fail",
    component: () =>
      import(/* webpackChunkName: "signin" */ "../views/SignInView.vue"),
    props: true,
    meta: { requiresAuth: false, title: "Sign In" }
  },
  {
    path: "/signout",
    name: "signout",
    component: () =>
      import(/* webpackChunkName: "signout" */ "../views/SignOutView.vue"),
    props: true,
    meta: { requiresAuth: true, title: "Sign Out" }
  },
  {
    path: "/signout/:redirectUrl",
    name: "signout-redirect",
    component: () =>
      import(/* webpackChunkName: "signout" */ "../views/SignOutView.vue"),
    props: true,
    meta: { requiresAuth: true, title: "Sign Out" }
  },
  {
    path: "/",
    name: "corpPartySearch",
    component: CorpPartySearch,
    meta: {
      title: "Director Search"
    }
  },
  {
    path: "/corpparty/:id",
    name: "corpPartyDetails",
    component: () =>
      import(
        /* webpackChunkName: "corppartydetails" */ "../views/CorpPartyDetails.vue"
      ),
    meta: {
      title: route => `Details for Filing #${route.params.id}`
    }
  },
  {
    path: "/corporation/:id",
    name: "corporationDetails",
    component: () =>
      import(
        /* webpackChunkName: "corporationdetails" */ "../views/CorporationDetails.vue"
      ),
    meta: {
      title: route => `Corporation Details for Inc. #${route.params.id}`
    }
  },
  {
    path: "/corporation",
    name: "corporation",
    component: () =>
      import(
        /* webpackChunkName: "corporation" */ "../views/CorporationSearch.vue"
      ),
    meta: {
      title: "Corporation Search"
    }
  },
  {
    path: "*",
    component: NotFound,
    meta: {
      title: "Director Search | Not Found"
    }
  }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

router.beforeEach((to, from, next) => {
  const query = Object.assign({}, to.query);
  const { title } = to.meta;
  document.title = typeof title === "function" ? title(to) : title;
  const KEYCLOACK_TOKEN = sessionStorage.getItem("KEYCLOAK_TOKEN");
  const CURRENT_ACCOUNT = sessionStorage.getItem("CURRENT_ACCOUNT");
  const CURRENT_ACCOUNT_ID = CURRENT_ACCOUNT
    ? JSON.parse(CURRENT_ACCOUNT).id
    : "";
  if (
    !KEYCLOACK_TOKEN &&
    to.name !== "signin" &&
    to.name !== "signin-redirect"
  ) {
    delete ApiService.defaults.headers.common["Authorization"];
    delete ApiService.defaults.headers.common["X-Account-Id"];
    next({
      name: "signin-redirect",
      query,
      params: {
        idpHint: "bcros",
        redirectUrl: to.path
      }
    });
  } else {
    ApiService.defaults.headers.common[
      "Authorization"
    ] = `Bearer ${KEYCLOACK_TOKEN}`;
    ApiService.defaults.headers["X-Account-Id"] = CURRENT_ACCOUNT_ID;
    next();
  }
});

export default router;
