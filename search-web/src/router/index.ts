import Vue from 'vue'
import VueRouter, { Route } from 'vue-router'
import { routes } from './routes'
import { SessionStorageKeys } from 'sbc-common-components/src/util/constants'
/**
 * Configures and returns Vue Router.
 */
export function getVueRouter () {
  Vue.use(VueRouter)

  const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
  })

  router.beforeEach((to, from, next) => {
    const query = Object.assign({}, to.query)
    const { title } = to.meta
    document.title = typeof title === 'function' ? title(to) : title

    if (!isAuthenticated() && !isSigninRoute(to) && !isSignRedirectRoute(to)) {
      next({
        name: 'signin-redirect',
        query,
        params: {
          idpHint: 'bcros',
          redirectUrl: to.path
        }
      })
    } else {
      next()
    }
  })

  /** Returns True if user is authenticated, else False. */
  function isAuthenticated (): boolean {
    // FUTURE: also check that token isn't expired!
    return Boolean(sessionStorage.getItem(SessionStorageKeys.KeyCloakToken))
  }

  /** Returns True if route is Signin, else False. */
  function isSigninRoute (route: Route): boolean {
    return Boolean(route.name === 'signin')
  }

  /** Returns True if route is Signin Redirect, else False. */
  function isSignRedirectRoute (route: Route): boolean {
    return Boolean(route.name === 'signin-redirect')
  }

  return router
}
