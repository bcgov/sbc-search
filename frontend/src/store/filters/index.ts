export default {
  namespaced: true,
  state: {
    filters: [{ uid: 0, field: "first_nme", operator: "exact", query: "" }]
  },
  mutations: {
    addFilter(state, filter) {
      state.filters.push(filter);
    },
    removeFilter(state, uid) {
      const result = state.filters.findIndex(f => f.uid === uid);
      if (result !== -1) {
        state.filters.splice(result, 1);
      }
      return;
    },
    setSearchQuery(state, { uid, query }) {
      const filter = state.filters.find(f => f.uid === uid);
      if (filter) {
        filter.query = query;
      }
    }
  },
  actions: {},
  getters: {
    getFilters(state) {
      return state.filters;
    },
    getFilter(state, uid) {
      return function(uid) {
        state.filters.find(f => f.uid === uid);
      };
    },
    getNumFilters(state) {
      return state.filters.length;
    }
  }
};
