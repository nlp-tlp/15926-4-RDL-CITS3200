import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import GraphView from '@/views/GraphView.vue'

vi.mock('vue-router', () => ({
  useRoute: vi.fn()
}))

describe('GraphSearchSidepane.vue', () => {
  it('renders the component', () => {
    const wrapper = mount(GraphView)
    const searchSidepane = wrapper.findComponent({ name: 'GraphSearchSidepane' })
    expect(searchSidepane.exists()).toBe(true)
  })

  it('does not render the sidepane by default', () => {
    const wrapper = mount(GraphView)
    const leftHeaderText = wrapper.find('.left-text')
    expect(leftHeaderText.exists()).toBe(false)
  })

  it('toggles rendering of sidepane contents when sidepane button is clicked', async () => {
    const wrapper = mount(GraphView)
    const sidepaneButton = wrapper.find('.left-btn')
    expect(sidepaneButton.isVisible()).toBe(true)
    expect(wrapper.find('.left-text').exists()).toBe(false)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.left-text').exists()).toBe(true)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.left-text').exists()).toBe(false)
  })
})
