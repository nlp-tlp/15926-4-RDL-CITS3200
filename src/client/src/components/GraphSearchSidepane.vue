<script setup lang="ts">
import { ref } from 'vue'

// Define props with default values using withDefaults (type-based declaration)
const props = withDefaults(
  defineProps<{
    /**
     * Determines if the side panel is initially expanded (default: false).
     */
    initialExpanded?: boolean
  }>(),
  {
    initialExpanded: false
  }
)

// Initialise isLeftExpanded with the value of initialExpanded prop
const isLeftExpanded = ref(props.initialExpanded)

function toggleLeftNav(): void {
  isLeftExpanded.value = !isLeftExpanded.value
}
</script>

<script lang="ts">
/**
 * GraphSearchSidepane component represents the expandable side panel containing search functionality.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 *
 * @example
 * <GraphSearchSidepane :initialExpanded="true" />
 * <GraphSearchSidepane initialExpanded />
 * <GraphSearchSidepane />
 */
export default {
  name: 'GraphSearchSidepane'
}
</script>

<template>
  <div :class="['left-sidepanel', { 'sidepanel-expanded': isLeftExpanded }]">
    <button class="left-btn" @click="toggleLeftNav">&#9776;</button>
    <p class="left-text">Left Sidepanel</p>
  </div>
</template>

<style scoped>
.left-sidepanel {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: 100%;
  width: 50px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  left: 0;
  background-color: transparent;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded {
  width: 250px;
  background-color: var(--color-nav-background);
}

.left-btn {
  position: absolute;
  top: 0.5rem;
  left: 0.5rem;
  background-color: transparent;
  color: var(--color-nav-background);
  transition:
    background-color 0.5s ease,
    color 0.5s ease;
  cursor: pointer;
  border: none;
  font-size: 22px;
  font-weight: bold;
}

.sidepanel-expanded .left-btn {
  background-color: var(--color-nav-background);
  color: white;
}

.left-text {
  margin: 0.75rem 1rem 0 auto;
  color: white;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
}

.sidepanel-expanded .left-text {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}
</style>
