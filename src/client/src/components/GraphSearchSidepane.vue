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
    <div class="left-header">
      <button class="left-btn" @click="toggleLeftNav">&#9776;</button>
      <p class="left-text">Left Sidepanel</p>
    </div>
  </div>
</template>

<style scoped>
.left-sidepanel {
  height: 100%;
  width: 50px;
  position: fixed;
  z-index: 1;
  top: 4.5rem;
  left: 0;
  background-color: white;
  overflow-x: hidden;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded {
  width: 250px;
  background-color: var(--color-nav-background);
}

.left-header {
  width: 100%;
  height: 60px;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  z-index: 2;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded .left-header {
  background-color: var(--color-nav-background);
  color: white;
}

.left-btn {
  margin-left: 10px;
  background-color: white;
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
  margin-right: 10px;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
  font-size: 16px;
  cursor: default;
}

.sidepanel-expanded .left-text {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}
</style>
