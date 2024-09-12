import { shallowMount } from '@vue/test-utils'
import { describe, expect, it, vi } from 'vitest'

import NavBar from '@/components/NavBar.vue'

vi.mock('vue-router', () => ({
  useRoute: vi.fn()
}))

const wrapper = shallowMount(NavBar)

describe('NavBar.vue', () => {
  it('renders the component', () => {
    expect(wrapper.exists()).toBe(true)
  })

  it('renders the site title', () => {
    const title = wrapper.find('#navbar-title')
    expect(title.text()).toBe('iso15926vis')
  })

  it('renders three nav items labelled home, graph and documentation', () => {
    const navItems = wrapper.findAllComponents({ name: 'NavBarItem' })
    expect(navItems.length).toBe(3) // home, graph, and documentation
    expect(navItems[0].props('label')).toBe('Home')
    expect(navItems[1].props('label')).toBe('Graph')
    expect(navItems[2].props('label')).toBe('Documentation')
  })
})
