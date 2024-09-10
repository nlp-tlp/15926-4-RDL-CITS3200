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

// Initialise isRightExpanded with the value of initialExpanded prop
const isRightExpanded = ref(props.initialExpanded)

function toggleRightNav(): void {
  isRightExpanded.value = !isRightExpanded.value
}
</script>

<script lang="ts">
/**
 * GraphInfoSidepane component represents the expandable side panel containing information functionality.
 *
 * @param {boolean} initialExpanded - Determines if the side panel is initially expanded (default: false).
 *
 * @example
 * <GraphInfoSidepane :initialExpanded="true" />
 * <GraphInfoSidepane initialExpanded />
 * <GraphInfoSidepane />
 */
export default {
  name: 'GraphInfoSidepane'
}
</script>

<template>
  <div :class="['right-sidepanel', { 'sidepanel-expanded': isRightExpanded }]">
    <button class="right-btn" @click="toggleRightNav">&#9776;</button>
    <p class="right-text">Right Sidepanel</p>
  </div>
</template>

<style scoped>
.right-sidepanel {
  display: flex;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: 100%;
  width: 50px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  right: 0;
  background-color: transparent;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded {
  width: 250px;
  background-color: var(--color-nav-background);
}

.right-btn {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
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

.sidepanel-expanded .right-btn {
  background-color: var(--color-nav-background);
  color: white;
}

.right-text {
  margin: 0.75rem 0 0 1rem;
  color: white;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
}

.sidepanel-expanded .right-text {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}
</style>
