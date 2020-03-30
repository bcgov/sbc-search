import { mount, shallowMount, createLocalVue } from "@vue/test-utils";
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

    const sampleData = {
        "NAMES": [
          {
            "name": "Yamana Gold Inc."
          }
        ], 
        "admin_email": null, 
        "corp_num": "7990123456", 
        "offices": [
          {
            "delivery_addr": "28 Helene St N, Mississauga, ON", 
            "email_address": null, 
            "mailing_addr": "28 Helene St N, Mississauga, ON", 
            "office_typ_cd": null
          }
        ], 
        "transition_dt": null
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
    
    it("renders details", () => {
        const wrapper = mount(CorporationDetailsView, {
        mocks: {
            $route
        },
        data: function() {
            return {
                details: sampleData
            }
        },
        localVue,
        vuetify
        });

        expect(wrapper.find(".details-corp-number").text()).toBe(sampleData.corp_num)

    })
});
