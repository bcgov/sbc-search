import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import CorporationSearchView from "@/views/CorporationSearch.vue"
import CorporationSearch from "@/components/Search/corporation/CorporationSearch.vue";
import SearchInput from "@/components/Search/corporation/SearchInput.vue";
import CorporationTable from "@/components/Search/corporation/CorporationTable.vue";
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";

Vue.use(Vuetify);

describe("Corporation Search", () => {
    const localVue = createLocalVue();
    localVue.use(Vuex);
    let vuetify = new Vuetify({});
    const $route = {
      query: {
          query: 'i',
          page: '1',
          sort_type: 'dsc',
          sort_value: 'corp_nme'
      },
    };

    it("renders a vue instance", () => {
        const wrapper = shallowMount(CorporationSearchView, {
          mocks: {
            $route
          },
          localVue,
          vuetify
        });
        expect(wrapper.isVueInstance()).toBe(true);
    });

    const wrapper = mount(CorporationSearchView, {
        mocks: {
          $route
        },
        localVue,
        vuetify
    });

    it("children are a vue instance", () => {
        expect(wrapper.find(CorporationSearch).isVueInstance()).toBe(true);
        expect(wrapper.find(CorporationTable).isVueInstance()).toBe(true);
        expect(wrapper.find(SearchInput).isVueInstance()).toBe(true);
    });
    
    it("sets search input correctly", () => {
        expect(wrapper.find(SearchInput).vm['searchQuery']).toBe($route.query.query)
    })
    
});
