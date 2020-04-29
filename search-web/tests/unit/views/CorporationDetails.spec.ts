import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import CorporationDetailsView from "@/views/CorporationDetails.vue";
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
  };

  const sampleData = {
    adminEmail: null,
    corpNum: "7890123456",
    names: [{ name: "Telus Corporation" }],
    offices: [
      {
        deliveryAddr: "109 Saskatchewan Blvd, Dauphin, MB",
        emailAddress: null,
        mailingAddr: "109 Saskatchewan Blvd, Dauphin, MB",
        officeTypCd: ""
      }
    ],
    transitionDt: null
  };

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

  it("renders details", () => {
    const wrapper = mount(CorporationDetailsView, {
      mocks: {
        $route
      },
      data: function() {
        return {
          details: sampleData
        };
      },
      localVue,
      vuetify
    });

    expect(wrapper.find(".details-corp-number").text()).toBe(
      sampleData['corpNum']
    );
  });
});
