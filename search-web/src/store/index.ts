import Vue from 'vue'
import Vuex from 'vuex'
import corpParty from './corpparty'
import corporation from './corporation'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: {
    corpParty,
    corporation
  }
})
