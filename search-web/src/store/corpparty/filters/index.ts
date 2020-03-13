export default {
  namespaced: true,
  state: {
    filters: [
      { uid: 0, field: "first_nme", operator: "exact", value: "" },
      { uid: 1, field: "last_nme", operator: "exact", value: "" }
    ]
  },
  mutations: {
    addFilter(state, filter) {
      state.filters.push(filter);
    },
    setFilters(state, filters) {
      state.filters = filters;
    },
    removeFilter(state, uid) {
      const result = state.filters.findIndex(f => f.uid === uid);
      if (result !== -1) {
        state.filters.splice(result, 1);
      }
      return;
    },
    setSearchValue(state, { uid, value }) {
      const filter = state.filters.find(f => f.uid === uid);
      if (filter) {
        filter.value = value;
      }
    },
    setSearchPropValue(state, { uid, property, value }) {
      const filter = state.filters.find(f => f.uid === uid);
      if (filter) {
        filter[property] = value;
      }
    }
  },
  actions: {},
  getters: {
    getFilters(state) {
      return state.filters;
    },
    getFilter: state => uid => {
      return state.filters.find(f => f.uid === uid);
    },
    getProperty: state => (uid, prop) => {
      const filter = state.filters.find(f => f.uid === uid);
      return filter && filter[prop];
    },
    getFilterValue: state => uid => {
      const filter = state.filters.find(f => f.uid === uid);
      return filter && filter.value;
    },
    getNumFilters(state) {
      return state.filters.length;
    }
  }
};
