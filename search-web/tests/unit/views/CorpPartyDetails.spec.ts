import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import CorpPartyDetailsView from "@/views/CorpPartyDetails.vue";
import Details from "@/components/Details/Details.vue";
import Vue from "vue";
import Vuetify from "vuetify";
import Vuex from "vuex";

Vue.use(Vuetify);

describe("CorpParty Details", () => {
  const localVue = createLocalVue();
  localVue.use(Vuex);
  let vuetify = new Vuetify({});
  const $route = {
    query: {},
    params: {
      id: null
    }
  };

  const detail = {
    "appointmentDt": "Mon, 06 Apr 2020 00:00:00 GMT", 
    "cessationDt": "Mon, 06 Apr 2020 00:00:00 GMT", 
    "corpAdminEmail": null, 
    "corpDeliveryAddr": "106 Saint-Georges Rue, La Prairie, QC", 
    "corpMailingAddr": "106 Saint-Georges Rue, La Prairie, QC", 
    "corpNme": "Imperial Oil", 
    "corpNum": "2345678901", 
    "corpPartyEmail": null, 
    "corpPartyId": 1, 
    "corpTypCd": "B", 
    "deliveryAddr": "106 Saint-Georges Rue, La Prairie, QC", 
    "firstNme": "abc", 
    "fullDesc": "Change of Head Office (NWPTA)", 
    "lastNme": "test", 
    "mailingAddr": "106 Saint-Georges Rue, La Prairie, QC", 
    "middleNme": "Patterson", 
    "offices": [
      {
        "appointmentDt": "Mon, 06 Apr 2020 00:00:00 GMT", 
        "corpPartyId": 1, 
        "officerTypCd": "SEC", 
        "shortDesc": "Secretary", 
        "year": null
      }, 
      {
        "appointmentDt": "Mon, 06 Apr 2020 00:00:00 GMT", 
        "corpPartyId": 1, 
        "officerTypCd": "INC", 
        "shortDesc": "Incorporator", 
        "year": null
      }
    ], 
    "partyTypCd": "DIR", 
    "sameAddr": [], 
    "sameNameAndCompany": [], 
    "states": [
      {
        "corpNum": "2345678901", 
        "ddCorpNum": null, 
        "endEventId": null, 
        "startEventId": 1, 
        "stateTypCd": "HIS"
      }
    ]
  }

  it("renders a vue instance", () => {
    const wrapper = shallowMount(CorpPartyDetailsView, {
      mocks: {
        $route
      },
      localVue,
      vuetify
    });
    expect(wrapper.isVueInstance()).toBe(true);
  });

  it("children are vue instance", () => {
    const wrapper = mount(CorpPartyDetailsView, {
      mocks: {
        $route,
      },
      data: function() {
        return {
          detail: detail
        };
      },
      localVue,
      vuetify
    });

    expect(wrapper.find(Details).isVueInstance()).toBe(true);
  });

  it("renders details", async () => {
    const wrapper = mount(CorpPartyDetailsView, {
      mocks: {
        $route
      },
      localVue,
      vuetify,
      data: function() {
        return {
          detail: detail
        };
      }
    });

    expect(wrapper.find(".detail-office-link").text()).toBe(
      detail.corpNme
    );
    expect(wrapper.find(".office-held-desc").text()).toBe(
      detail.offices[0].shortDesc
    );
  });
});
