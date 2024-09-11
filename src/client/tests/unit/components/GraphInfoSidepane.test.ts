import { mount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import GraphView from '@/views/GraphView.vue'

vi.mock('vue-router', () => ({
  useRoute: vi.fn()
}))

describe('GraphSearchSidepane.vue', () => {
  it('renders the component', () => {
    const wrapper = mount(GraphView)
    const infoSidepane = wrapper.findComponent({ name: 'GraphInfoSidepane' })
    expect(infoSidepane.exists()).toBe(true)
  })

  it('does not render the sidepane by default', () => {
    const wrapper = mount(GraphView)
    const rightHeaderText = wrapper.find('.right-text')
    expect(rightHeaderText.exists()).toBe(false)
  })

  it('toggles rendering of sidepane contents when sidepane button is clicked', async () => {
    const wrapper = mount(GraphView)
    const sidepaneButton = wrapper.find('.right-btn')
    expect(sidepaneButton.isVisible()).toBe(true)
    expect(wrapper.find('.right-text').exists()).toBe(false)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.right-text').exists()).toBe(true)

    await sidepaneButton.trigger('click')
    await wrapper.vm.$nextTick()
    expect(wrapper.find('.right-text').exists()).toBe(false)
  })
})
