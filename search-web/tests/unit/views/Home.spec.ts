import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import Home from "@/views/Home.vue";
import CorpPartySearch from "@/components/Search/corpparty/CorpPartySearch.vue"
import SearchInput from "@/components/Search/corpparty/SearchInput.vue"
import store from "@/store/index";
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";

Vue.use(Vuetify);

describe("Home.vue", () => {
  const localVue = createLocalVue();
  localVue.use(Vuex);

  let vuetify = new Vuetify({});
  const $route = {
    query: {}
  };

  it("renders a vue instance", () => {
    const wrapper = shallowMount(Home, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    });
    expect(wrapper.isVueInstance()).toBe(true);
  });

  it("render a title", async () => {
    const wrapper = shallowMount(Home, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    });
    wrapper.setData({ title: "Welcome to Director Search Test" });
    Vue.nextTick(() => {
      expect(wrapper.find(".home-title").text()).toBe(
        "Welcome to Director Search Test"
      );
    });
  });

  it("renders search tips", () => {
    const wrapper = mount(Home, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    });
    expect(wrapper.find(".search-tips-header").text());
  }),
    it("renders filters from query string", async () => {
      const $route = {
        query: {
          field: ["first_nme", "last_nme"],
          operator: ["exact", "contains"],
          value: ["Clark", "Van Oyen"],
          mode: "ALL",
          additional_cols: "none",
          page: "1",
          sort_type: "dsc",
          sort_value: "last_nme"
        }
      };
      const wrapper = mount(Home, {
        store,
        mocks: {
          $route
        },
        localVue,
        vuetify,
        stubs: {
          CorpPartyTable: true
        }
      });
      await localVue.nextTick()
      const corpPartySearch = wrapper.findAll(CorpPartySearch);
      expect(corpPartySearch.at(0).vm['selectedField']).toBe('first_nme')
      expect(corpPartySearch.at(1).vm['selectedField']).toBe('last_nme')
      expect(corpPartySearch.at(0).vm['selectedOperator']).toBe('exact')
      expect(corpPartySearch.at(1).vm['selectedOperator']).toBe('contains')

      const searchInput = wrapper.findAll(SearchInput);
      expect(searchInput.at(0).vm['searchQuery']).toBe('Clark')
      expect(searchInput.at(1).vm['searchQuery']).toBe('Van Oyen')
     

      expect(wrapper.vm["filters"][0]).toEqual({
        uid: 1,
        field: "first_nme",
        operator: "exact",
        value: "Clark"
      });
      expect(wrapper.vm["filters"][1]).toEqual({
        uid: 2,
        field: "last_nme",
        operator: "contains",
        value: "Van Oyen"
      });
    });
});
