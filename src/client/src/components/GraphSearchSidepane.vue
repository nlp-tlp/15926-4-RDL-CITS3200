<script setup lang="ts">
import { ref } from 'vue'

const isLeftExpanded = ref(false)

function toggleLeftNav() {
  isLeftExpanded.value = !isLeftExpanded.value
}

const selectedSearchType = ref('id')
const showDeprecated = ref(false)
const viewLabelsInGraph = ref(true)
const levelsAbove = ref(0)
const levelsBelow = ref(0)
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
    <div class="left-header">
      <button class="left-btn" @click="toggleLeftNav">&#9776;</button>
      <p v-if="isLeftExpanded" class="left-text">Graph Search</p>
    </div>

    <transition name="fade-slide">
      <div v-if="isLeftExpanded" class="search-bar">
        <input type="text" placeholder="Search..." />
      </div>
    </transition>

    <transition name="fade-slide">
      <div v-if="isLeftExpanded" class="dropdown">
        <label for="search-type">Search by:</label>
        <select id="search-type" v-model="selectedSearchType">
          <option value="id">ID / URI</option>
          <option value="label">RDF Label</option>
        </select>
      </div>
    </transition>

    <transition name="fade-slide">
      <div v-if="isLeftExpanded" class="toggles">
        <label>
          <input type="checkbox" v-model="showDeprecated" />
          Show Deprecated
        </label>
        <label>
          <input type="checkbox" v-model="viewLabelsInGraph" />
          View Labels in Graph
        </label>
      </div>
    </transition>

    <transition name="fade-slide">
      <div v-if="isLeftExpanded" class="levels-input">
        <div class="input-group">
          <label>Levels Above:</label>
          <input type="number" v-model="levelsAbove" min="0" max="6" />
        </div>
        <div class="input-group">
          <label>Levels Below:</label>
          <input type="number" v-model="levelsBelow" min="0" max="6" />
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}

.fade-slide-enter,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(0px);
}

.left-sidepanel {
  height: 100%;
  width: 50px;
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

.search-bar {
  padding: 10px;
}

.search-bar input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
}

.dropdown {
  padding: 10px;
  margin-bottom: 20px;
  margin-top: -8px;
}

.dropdown label {
  display: block;
  margin-bottom: 5px;
  color: white;
}

.dropdown select {
  width: 100%;
  padding: 8px;
  font-size: 14px;
}

.toggles {
  padding: 10px;
  margin-bottom: 20px;
}

.toggles label {
  width: 100%;
  display: block;
  margin-bottom: 10px;
  color: white;
}

.levels-input {
  padding: 10px;
  display: flex;
  justify-content: space-between;
}

.input-group {
  display: flex;
  flex-direction: column;
  width: 48%;
}

.input-group label {
  margin-bottom: 5px;
  color: white;
}

.input-group input {
  width: 100%;
  padding: 8px;
  font-size: 14px;
}
</style>
