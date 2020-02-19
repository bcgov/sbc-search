import Vue from "vue";
import Vuex from "vuex";
import { isEqual } from "lodash-es";

Vue.use(Vuex);

export default new Vuex.Store({
  state: {
    filters: []
  },
  mutations: {
    addFilter(state, filter) {
      state.filters.push(filter);
    },
    removeFilter(state, filter) {
      const result = state.filters.findIndex(f => isEqual(f, filter));
      if (result !== -1) {
        return state.filters.splice(result, 1);
      }
      return;
    },
    setFilter(state, filters) {
      state.filters = filters;
    }
  },
  actions: {},
  modules: {}
});
