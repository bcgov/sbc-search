import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
import CorpPartyDetailsView from "@/views/CorpPartyDetails.vue"
import Details from "@/components/Details/Details.vue"
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

    const sampleDetails = {
        "appointment_dt": "Tue, 25 Feb 2020 00:00:00 GMT", 
        "cessation_dt": "Tue, 25 Feb 2020 00:00:00 GMT", 
        "corp_admin_email": null, 
        "corp_delivery_addr": "1586 Des Erables Rue, Chicoutimi, QC", 
        "corp_mailing_addr": "1586 Des Erables Rue, Chicoutimi, QC", 
        "corp_nme": "Loblaw Companies", 
        "corp_num": "4567890123", 
        "corp_party_email": null, 
        "corp_party_id": 3, 
        "corp_typ_cd": "C", 
        "delivery_addr": "1586 Des Erables Rue, Chicoutimi, QC", 
        "first_nme": "Hadley", 
        "full_desc": "Certificate of Good Standing", 
        "last_nme": "Sanford", 
        "mailing_addr": "1586 Des Erables Rue, Chicoutimi, QC", 
        "middle_nme": null, 
        "party_typ_cd": "FIO", 
        "states": [
            {
            "corp_num": "4567890123", 
            "dd_corp_num": null, 
            "end_event_id": null, 
            "start_event_id": 1, 
            "state_typ_cd": "HIS"
            }
        ]
    }

    const sampleOffices = {
        "offices": [
          {
            "appointment_dt": "Tue, 25 Feb 2020 00:00:00 GMT", 
            "corp_party_id": 3, 
            "officer_typ_cd": "SEC", 
            "short_desc": "Secretary", 
            "year": null
          }, 
          {
            "appointment_dt": "Tue, 25 Feb 2020 00:00:00 GMT", 
            "corp_party_id": 3, 
            "officer_typ_cd": "DIR", 
            "short_desc": "Director", 
            "year": null
          }
        ], 
        "same_addr": [], 
        "same_name_and_company": []
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
        const wrapper = shallowMount(CorpPartyDetailsView, {
            mocks: {
              $route
            },
            localVue,
            vuetify
        });
        expect(wrapper.find(Details).isVueInstance()).toBe(true);
    })

    it("renders details", async () => {
        const wrapper = mount(CorpPartyDetailsView, {
            mocks: {
              $route
            },
            localVue,
            vuetify,
            data: function() { 
            return {
                detail: sampleDetails,
                officesheld: sampleOffices
            }
            }
        });
        
        expect(wrapper.find(".detail-office-link").text()).toBe(sampleDetails.corp_nme)
        expect(wrapper.find(".office-held-desc").text()).toBe(sampleOffices.offices[0].short_desc)
    })
});
