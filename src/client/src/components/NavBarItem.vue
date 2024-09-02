<script setup lang="ts">
import { computed } from 'vue'
import { RouterLink } from 'vue-router'

const props = defineProps({
  to: {
    type: String,
    required: true
  },
  label: {
    type: String,
    required: true
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
  <!-- If it's an external link -->
  <a v-if="isExternalLink" :href="to" class="navbar-item" target="_blank" rel="noopener noreferrer">
    <slot name="icon"></slot>
    {{ label }}
  </a>

  <!-- If it's an internal link -->
  <RouterLink v-else :to="to" class="navbar-item">
    <slot name="icon"></slot>
    {{ label }}
  </RouterLink>
</template>

<style scoped>
.navbar-item {
  display: flex;
  align-items: center;
  text-decoration: none;
  text-align: center;
  padding: 0 1rem;
  border-left: 2px solid var(--color-border);
  color: var(--color-nav-text);
}
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
