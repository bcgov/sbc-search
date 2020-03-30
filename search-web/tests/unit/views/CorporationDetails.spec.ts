import { shallowMount, createLocalVue } from "@vue/test-utils";
import CorporationDetailsView from "@/views/CorporationDetails.vue"
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";

Vue.use(Vuetify);

describe("Corporation Details", () => {
    const localVue = createLocalVue();
    localVue.use(Vuex);
    let vuetify = new Vuetify({});
    const $route = {
        params: {
            id: null
        }
    }
 
    it("renders a vue instance", () => {
        const wrapper = shallowMount(CorporationDetailsView, {
          mocks: {
            $route
          },
          localVue,
          vuetify
        });
        expect(wrapper.isVueInstance()).toBe(true);
    });
});
