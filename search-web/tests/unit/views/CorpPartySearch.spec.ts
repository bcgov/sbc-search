import { mount, shallowMount, createLocalVue } from '@vue/test-utils'
import CorpPartySearchView from '@/views/CorpPartySearch.vue'
import CorpPartySearch from '@/components/Search/corpparty/CorpPartySearch.vue'
import SearchInput from '@/components/Search/corpparty/SearchInput.vue'
import CorpPartyTable from '@/components/Search/corpparty/CorpPartyTable.vue'
import store from '@/store/index'
import Vue from 'vue'
import Vuetify from 'vuetify'
import Vuex from 'vuex'
import omit from 'lodash-es/omit'

Vue.use(Vuetify)

describe('CorpPartySearch', () => {
  const localVue = createLocalVue()
  localVue.use(Vuex)

  let vuetify = new Vuetify({})
  const $route = {
    query: {}
  }

  it('renders a vue instance', () => {
    const wrapper = shallowMount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    })
    expect(wrapper.isVueInstance()).toBe(true)
  })

  it('render a title', async () => {
    const wrapper = shallowMount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    })
    wrapper.setData({ title: 'Welcome to Director Search Test' })
    Vue.nextTick(() => {
      expect(wrapper.find('.home-title').text()).toBe(
        'Welcome to Director Search Test'
      )
    })
  })

  it('renders search tips', () => {
    const wrapper = mount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    })
    expect(wrapper.find('.search-tips-header').text())
  })

  it('renders filters from query string', async () => {
    const $route = {
      query: {
        field: ['firstNme', 'lastNme'],
        operator: ['exact', 'contains'],
        value: ['Clark', 'Van Oyen'],
        mode: 'ALL',
        additional_cols: 'none',
        page: '1',
        sort_type: 'dsc',
        sort_value: 'lastNme'
      }
    }
    const wrapper = mount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify,
      stubs: {
        CorpPartyTable: true
      }
    })
    await localVue.nextTick()
    const corpPartySearch = wrapper.findAll(CorpPartySearch)
    expect(corpPartySearch.at(0).vm['selectedField']).toBe('firstNme')
    expect(corpPartySearch.at(1).vm['selectedField']).toBe('lastNme')
    expect(corpPartySearch.at(0).vm['selectedOperator']).toBe('exact')
    expect(corpPartySearch.at(1).vm['selectedOperator']).toBe('contains')

    const searchInput = wrapper.findAll(SearchInput)
    expect(searchInput.at(0).vm['searchQuery']).toBe('Clark')
    expect(searchInput.at(1).vm['searchQuery']).toBe('Van Oyen')

    expect(omit(wrapper.vm['filters'][0], 'uid')).toEqual({
      field: 'firstNme',
      operator: 'exact',
      value: 'Clark'
    })
    expect(omit(wrapper.vm['filters'][1], 'uid')).toEqual({
      field: 'lastNme',
      operator: 'contains',
      value: 'Van Oyen'
    })
  })

  it('renders table', async () => {
    const $route = {
      query: {
        field: ['firstNme', 'lastNme'],
        operator: ['exact', 'contains'],
        value: ['Clark', 'Van Oyen'],
        mode: 'ALL',
        additional_cols: 'none',
        page: '1',
        sort_type: 'dsc',
        sort_value: 'lastNme'
      }
    }
    const wrapper = mount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    })
    await localVue.nextTick()

    const corpPartyTable = wrapper.find(CorpPartyTable)
    expect(corpPartyTable.isVueInstance()).toBe(true)
    expect(corpPartyTable.find('.corp-party-table').exists()).toBe(true)
  })

  it('does not render a table', async () => {
    const wrapper = mount(CorpPartySearchView, {
      store,
      mocks: {
        $route
      },
      localVue,
      vuetify
    })
    await localVue.nextTick()

    const corpPartyTable = wrapper.find(CorpPartyTable)
    expect(corpPartyTable.isVueInstance()).toBe(true)
    expect(corpPartyTable.find('.corp-party-table').exists()).toBe(false)
  })
})
