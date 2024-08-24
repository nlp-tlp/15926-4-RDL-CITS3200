<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <RouterLink :to="to" class="navbar-item">
    <slot name="icon"></slot>
    {{ label }}
  </RouterLink>
</template>

<script lang="ts">
/**
 * NavBarItem component represents a navigation item in a navbar.
 *
 * @param {string} to - The route path for the navigation item.
 * @param {string} label - The label text displayed for the navigation item.
 *
 * @example
 * <NavBarItem to="/home" label="Home">
 *   <template #icon> (OPTIONAL ICON)
 *     <HomeIcon />
 *   </template>
 * </NavBarItem>
 */
export default {
  name: 'NavBarItem',
  props: {
    to: {
      type: String,
      required: true
    },
    label: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.navbar-item {
  display: flex;
  align-items: center;
  text-decoration: none;
  font-size: 1.1rem;
  text-align: center;
  padding: 0 1rem;
  border-left: 2px solid var(--color-border);
  color: var(--color-nav-text);
}
.navbar-item:first-of-type {
  border: 0;
}

.navbar-item.router-link-exact-active {
  color: var(--color-text);
}

.navbar-item.router-link-exact-active:hover {
  background-color: transparent;
}
</style>
