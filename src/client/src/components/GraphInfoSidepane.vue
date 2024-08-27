<script setup lang="ts">
import { ref } from 'vue'

/**
 * GraphInfoSidepane component represents the right side panel in the graph view.
 *
 * This component is used to display an expandable side panel on the right side of the graph view.
 * The panel can be toggled open or closed by clicking the associated button.
 *
 *
 * @function toggleRightNav
 * Toggles the right side panel between expanded and collapsed states.
 *
 * This function inverts the value of `isRightExpanded`. When the button associated
 * with the side panel is clicked, `toggleRightNav` is called, changing the panel's
 * state from open to closed or from closed to open.
 *
 * @prop {boolean} isRightExpanded - Indicates whether the right side panel is expanded.
 * This prop controls the expansion state of the side panel.
 *
 * @example
 * // Example usage within the template
 * <button @click="toggleRightNav">Toggle Right Panel</button>
 *
 * <div :class="{ 'right-sidepanel-expanded': isRightExpanded }">
 *   <!-- Content of the side panel -->
 * </div>
 */
const isRightExpanded = ref(false)

function toggleRightNav() {
  isRightExpanded.value = !isRightExpanded.value
}
</script>

<template>
  <div :class="['right-sidepanel', { 'right-sidepanel-expanded': isRightExpanded }]"></div>

  <button class="right-openbtn" @click="toggleRightNav">
    <span class="sidepane-label">Right Sidepanel</span>
    <span class="button-symbol">&#9776;</span>
  </button>
</template>

<style scoped>
.right-sidepanel {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 130px;
  right: 0;
  background-color: var(--color-nav-background);
  overflow: hidden;
  padding-top: 60px;
  transition:
    width 0.5s ease,
    transform 0.5s ease;
  transform: translateX(100%);
}

.right-sidepanel-expanded {
  width: 250px;
  transform: translateX(0);
}

.right-openbtn {
  width: 50px;
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px 0;
  border: none;
  position: fixed;
  top: 74px;
  right: 0;
  display: flex;
  align-items: center;
  padding-right: 250px;
  transform: translateX(0);
  transition:
    width 0.5s ease,
    transform 0.5s ease,
    background-color 0.5s ease,
    color 0.5s ease;
  z-index: 2;
}

.button-symbol {
  display: inline-block;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  margin-left: 20px;
}

.sidepane-label {
  display: inline-block;
  transition:
    opacity 2s ease,
    transform 0.5s ease;
  margin-left: 35px;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
}

.right-sidepanel-expanded + .right-openbtn {
  width: 250px;
  background-color: var(--color-nav-background);
  color: white;
  text-align: right;
  padding-right: 0;
  transform: translateX(0);
}

.right-sidepanel-expanded + .right-openbtn .sidepane-label {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.right-openbtn:hover {
  cursor: pointer;
}
</style>
