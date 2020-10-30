import CorpPartySearch from '../views/CorpPartySearch.vue'
import NotFound from '../views/NotFound.vue'
import SigninView from '../views/SignInView.vue'
import SignoutView from '../views/SignOutView.vue'

export const routes = [
  {
    path: '/signin/:idpHint',
    name: 'signin',
    component: SigninView,
    props: true,
    meta: { requiresAuth: false, title: 'Sign In' }
  },
  {
    path: '/signin/:idpHint/:redirectUrl',
    name: 'signin-redirect',
    component: SigninView,
    props: true,
    meta: { requiresAuth: false, title: 'Sign In' }
  },
  {
    path: '/signin/:idpHint/:redirectUrl/:redirectUrlLoginFail',
    name: 'signin-redirect-fail',
    component: SigninView,
    props: true,
    meta: { requiresAuth: false, title: 'Sign In' }
  },
  { path: '/signout',
    name: 'signout',
    component: SignoutView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/signout/:redirectUrl',
    name: 'signout-redirect',
    component: SignoutView,
    props: true,
    meta: { requiresAuth: true }
  },
  {
    path: '/',
    name: 'corpPartySearch',
    component: CorpPartySearch,
    meta: {
      title: 'Director Search'
    }
  },
  {
    path: '/corpparty/:id',
    name: 'corpPartyDetails',
    component: () =>
      import(
        /* webpackChunkName: "corppartydetails" */ '../views/CorpPartyDetails.vue'
      ),
    meta: {
      title: route => `Details for Filing #${route.params.id}`
    }
  },
  {
    path: '/corporation/:id',
    name: 'corporationDetails',
    component: () =>
      import(
        /* webpackChunkName: "corporationdetails" */ '../views/CorporationDetails.vue'
      ),
    meta: {
      title: route => `Corporation Details for Inc. #${route.params.id}`
    }
  },
  {
    path: '/corporation',
    name: 'corporation',
    component: () =>
      import(
        /* webpackChunkName: "corporation" */ '../views/CorporationSearch.vue'
      ),
    meta: {
      title: 'Corporation Search'
    }
  },
  {
    path: '*',
    component: NotFound,
    meta: {
      title: 'Director Search | Not Found'
    }
  }
]
