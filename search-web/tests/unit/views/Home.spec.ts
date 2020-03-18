import { shallowMount } from "@vue/test-utils"
import Home from "@/views/Home.vue"


describe('Foo', () => {
  it('renders a div', () => {
    const wrapper = shallowMount(Home)
    expect(wrapper.contains('div')).toBe(true)
  })
})