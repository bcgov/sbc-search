import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    filters: []
  },
  mutations: {
    addFilter(state, filter) {
      state.filters.push(filter);
    }
  },
  actions: {},
  modules: {}
});
