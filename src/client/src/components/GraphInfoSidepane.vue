<script setup lang="ts">
import { ref } from 'vue'

const isRightExpanded = ref(false)

function toggleRightNav() {
  isRightExpanded.value = !isRightExpanded.value
}
</script>

<script lang="ts">
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
export default {
  name: 'GraphInfoSidepane',
  props: {
    isRightExpanded: {
      type: Boolean,
      default: false
    }
  },
  emits: ['update:isRightExpanded'],
  methods: {
    toggleRightNav() {
      this.$emit('update:isRightExpanded', !this.isRightExpanded)
    }
  }
}
</script>

<template>
  <div :class="['right-sidepanel', { 'sidepanel-expanded': isRightExpanded }]">
    <button class="openbtn">
      <span class="sidepane-label">Right Sidepanel</span>
      <span class="button-symbol" @click="toggleRightNav">&#9776;</span>
    </button>
  </div>
</template>

<style scoped>
.right-sidepanel {
  height: 100%;
  width: 50px; /* Initial width when collapsed */
  position: fixed;
  top: 70px;
  right: 0;
  background-color: white;
  overflow-x: hidden;
  transition:
    width 0.5s ease,
    background-color 0.5s ease;
  z-index: 1;
}

.sidepanel-expanded {
  width: 250px; /* Expanded width when panel is open */
  background-color: var(--color-nav-background); /* Expanded background color */
}

.openbtn {
  width: 100%; /* Full width of the panel */
  height: 60px;
  font-size: 22px;
  font-weight: bold;
  background-color: white;
  color: var(--color-nav-background);
  padding: 10px;
  border: none;
  display: flex;
  align-items: center;
  justify-content: flex-end; /* Align items to the end */
  transition:
    background-color 0.5s ease,
    color 0.5s ease;
  z-index: 2;
}

.sidepanel-expanded .openbtn {
  background-color: var(--color-nav-background);
  color: white;
}

.button-symbol {
  margin-left: 10px; /* Margin between symbol and label */
  transition:
    opacity 0.5s ease,
    transform 0.5s ease;
  cursor: pointer; /* Add cursor pointer for symbol */
}

.sidepane-label {
  display: inline-block;
  margin-left: 10px; /* Margin between symbol and label */
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
</style>
