import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import GraphView from '@/views/GraphView.vue'

vi.mock('vue-router', () => ({
  useRoute: vi.fn()
}))

describe('GraphView.vue', () => {
  it('renders the GraphSearchSidepane component', () => {
    const wrapper = mount(GraphView)
    const searchSidepane = wrapper.findComponent({ name: 'GraphSearchSidepane' })
    expect(searchSidepane.exists()).toBe(true)
  })

  it('does not render the left header text by default', () => {
    const wrapper = mount(GraphView)
    const leftHeaderText = wrapper.find('.left-sidebar')
    expect(leftHeaderText.exists()).toBe(false)
  })

  it('toggles rendering of sidepane contents when sidepane button is clicked', async () => {
    const wrapper = mount(GraphView)
    const sidepaneButton = wrapper.find('.left-btn')
    expect(sidepaneButton.exists()).toBe(true)
    expect(wrapper.find('.left-sidebar').exists()).toBe(false)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.left-sidebar').exists()).toBe(true)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.left-sidebar').exists()).toBe(false)
  })
})
