<script setup lang="ts">
import { RouterLink } from 'vue-router'

interface NavBarItemProps {
  to: string
  label: string
}

const props = defineProps<NavBarItemProps>()
</script>

<template>
  <RouterLink :to="props.to" class="navbar-item">
    <slot name="icon"></slot>
    {{ props.label }}
  </RouterLink>
</template>

<style scoped>
.navbar-item {
  display: inline-block;
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
