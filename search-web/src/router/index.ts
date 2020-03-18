import Vue from "vue";
import VueRouter from "vue-router";
import Home from "../views/Home.vue";

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
  }
];

const router = new VueRouter({
  mode: "history",
  routes
});

router.beforeEach((to, from, next) => {
  const { title } = to.meta;
  document.title = typeof title === "function" ? title(to) : title;
  next();
});

export default router;
