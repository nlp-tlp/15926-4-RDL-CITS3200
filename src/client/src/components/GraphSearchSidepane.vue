<script setup lang="ts">
import { ref } from 'vue'

const isLeftExpanded = ref(false)

function toggleLeftNav() {
  isLeftExpanded.value = !isLeftExpanded.value
}
</script>

<script lang="ts">
/**
 * GraphSearchSidepane component represents the left side panel in the graph view.
 *
 * This component provides an expandable side panel on the left side of the graph view.
 * The panel can be toggled open or closed by clicking the associated button.
 *
 * @function toggleLeftNav
 * Toggles the left side panel between expanded and collapsed states.
 *
 * This method inverts the value of `isLeftExpanded`. When the button associated
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
 * <div :class="{ 'left-sidepanel-expanded': isLeftExpanded }">
 *   <!-- Content of the side panel -->
 * </div>
 */

export default {
  name: 'GraphSearchSidepane',
  props: {
    isLeftExpanded: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:isLeftExpanded'],
  methods: {
    /**
     * Toggles the left side panel between expanded and collapsed states.
     * Emits an event to update the `isLeftExpanded` prop.
     */
    toggleLeftNav() {
      this.$emit('update:isLeftExpanded', !this.isLeftExpanded)
    }
  }
}
</script>

<template>
  <div :class="['left-sidepanel', { 'sidepanel-expanded': isLeftExpanded }]">
    <button class="left-openbtn">
      <span class="button-symbol" @click="toggleLeftNav">&#9776;</span>
      <span class="sidepane-label">Left Sidepanel</span>
    </button>
  </div>
</template>

<style scoped>
.left-sidepanel {
  height: 100%;
  width: 50px; /* Initial width with button visible */
  position: fixed;
  z-index: 1;
  top: 70px;
  left: 0;
  background-color: white;
  overflow-x: hidden;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
}

.sidepanel-expanded {
  width: 250px; /* Expanded width when panel is open */
  background-color: var(--color-nav-background);
}

.left-openbtn {
  width: 100%; /* Button takes the full width of the panel */
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  cursor: pointer;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px 0;
  border: none;
  padding-left: 10px;
  display: flex;
  align-items: center;
  justify-content: flex-start;
  transition:
    background-color 0.5s ease,
    color 0.5s ease;
  z-index: 2;
}

.sidepanel-expanded .left-openbtn {
  background-color: var(--color-nav-background);
  color: white;
}

.button-symbol {
  margin-left: 10px;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
}

.sidepane-label {
  display: inline-block;
  margin-left: 10px;
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  opacity: 0;
  visibility: hidden;
  white-space: nowrap;
}

.sidepanel-expanded .sidepane-label {
  opacity: 1;
  visibility: visible;
  transform: translateX(0);
}

.left-openbtn:hover {
  cursor: pointer;
}
</style>
