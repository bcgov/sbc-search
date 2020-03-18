import { shallowMount, createLocalVue } from "@vue/test-utils";
import Home from "@/views/Home.vue";
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

  it("renders a div", () => {
    const wrapper = shallowMount(Home, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    });
    expect(wrapper.contains("div")).toBe(true);
  });
});
