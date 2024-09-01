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
    <div class="right-header">
      <p class="right-text">Right Sidepanel</p>
      <button class="right-btn" @click="toggleRightNav">&#9776;</button>
    </div>
  </div>
</template>

<style scoped>
.right-sidepanel {
  height: 100%;
  width: 50px;
  position: fixed;
  z-index: 1;
  top: 4.5rem;
  right: 0;
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

.right-header {
  width: 100%;
  height: 60px;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  z-index: 2;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded .right-header {
  background-color: var(--color-nav-background);
  color: white;
}

.right-btn {
  margin-right: 10px;
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

.sidepanel-expanded .right-btn {
  background-color: var(--color-nav-background);
  color: white;
}

.right-text {
  margin-left: 10px;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
  font-size: 16px;
  cursor: default;
}

.sidepanel-expanded .right-text {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}
</style>
