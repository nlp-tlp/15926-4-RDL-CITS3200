<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  /**
   * The route path or URL for the navigation item.
   */
  to: {
    type: String,
    required: true
  },
  /**
   * The label text displayed for the navigation item.
   */
  label: {
    type: String,
    required: true
  },
  /**
   * Optional custom class for the navigation item.
   */
  class: {
    type: String,
    default: ''
  }
})

const isExternalLink = computed(() => props.to.startsWith('http'))
</script>

<script lang="ts">
/**
 * NavBarItem component represents a navigation item in a navbar.
 *
 * @param {string} to - The route path or URL for the navigation item.
 * @param {string} label - The label text displayed for the navigation item.
 * @param {string} class - Optional custom class for additional styling.
 *
 * @slot `icon` - Optional slot for an icon to display with the navigation item.
 *
 * @example
 * <NavBarItem to="/home" label="Home">
 *   <template #icon> (OPTIONAL ICON)
 *     <HomeIcon />
 *   </template>
 * </NavBarItem>
 */
export default {
  name: 'NavBarItem'
}
</script>

<template>
  <a
    v-if="isExternalLink"
    :href="to"
    :class="[
      'navbar-item',
      props.class,
      'flex items-center no-underline text-center text-nav-text px-4 rounded-md hover:bg-cyan-950 transition duration-400 p-1'
    ]"
    target="_blank"
    rel="noopener noreferrer"
  >
    <slot name="icon"></slot>
    <div>
      {{ label }}
    </div>
  </a>

  <RouterLink
    v-else
    :to="to"
    :class="[
      'navbar-item',
      props.class,
      'flex items-center no-underline text-center text-nav-text px-4 rounded-md hover:bg-cyan-950 transition duration-400 p-1'
    ]"
  >
    <slot name="icon"></slot>
    <div class="hidden sm:inline">
      {{ label }}
    </div>
  </RouterLink>
</template>

<style scoped>
.navbar-item:first-of-type {
  border: 0;
}

.navbar-item.router-link-exact-active {
  color: var(--color-nav-text-active);
}

.navbar-item.router-link-exact-active:hover {
  background-color: transparent;
}
</style>
