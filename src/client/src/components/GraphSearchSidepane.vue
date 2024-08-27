<script setup lang="ts">
import { ref } from 'vue'

/**
 * GraphSearchSidepane component represents the left side panel in the graph view.
 *
 * This component is used to display an expandable side panel on the left side of the graph view.
 * The panel can be toggled open or closed by clicking the associated button.
 *
 * @function toggleLeftNav
 * Toggles the left side panel between expanded and collapsed states.
 *
 * This function inverts the value of `isLeftExpanded`. When the button associated
 * with the side panel is clicked, `toggleLeftNav` is called, changing the panel's
 * state from open to closed or from closed to open.
 *
 * @prop {boolean} isLeftExpanded - Indicates whether the left side panel is expanded.
 * This prop controls the expansion state of the side panel.
 *
 * @example
 * // Example usage within the template
 * <button @click="toggleLeftNav">Toggle Left Panel</button>
 *
 * <div :class="{ 'sidepanel-expanded': isLeftExpanded }">
 *   <!-- Content of the side panel -->
 * </div>
 */
const isLeftExpanded = ref(false)

function toggleLeftNav() {
  isLeftExpanded.value = !isLeftExpanded.value
}
</script>

<template>
  <div :class="['left-sidepanel', { 'sidepanel-expanded': isLeftExpanded }]"></div>

  <button class="left-openbtn" @click="toggleLeftNav">
    <span class="button-symbol">&#9776;</span>
    <span class="sidepane-label">Left Sidepanel</span>
  </button>
</template>

<style scoped>
.left-sidepanel {
  height: 100%;
  width: 0;
  position: fixed;
  z-index: 1;
  top: 130px;
  left: 0;
  background-color: var(--color-nav-background);
  overflow-x: hidden;
  padding-top: 60px;
  transition:
    width 0.5s ease,
    transform 0.5s ease;
  transform: translateX(-100%);
}

.sidepanel-expanded {
  width: 250px;
  transform: translateX(0); /* Synchronize with button's movement */
}

.left-openbtn {
  width: 50px;
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px 0;
  border: none;
  position: absolute;
  top: 74px;
  left: 0;
  display: flex;
  align-items: center;
  transform: translateX(30px);
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
}

.sidepane-label {
  display: inline-block;
  margin-left: 10px;
  transition:
    opacity 0.8s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
}

.sidepanel-expanded + .left-openbtn {
  width: 250px;
  background-color: var(--color-nav-background);
  color: white;
  text-align: left;
  padding-left: 15px;
  transform: translateX(0); /* Synchronize with panel expansion */
}

.sidepanel-expanded + .left-openbtn .sidepane-label {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.left-openbtn:hover {
  cursor: pointer;
}
</style>
