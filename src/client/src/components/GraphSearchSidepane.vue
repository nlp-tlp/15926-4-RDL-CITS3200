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
    <p class="left-text">Graph Search</p>

    <div v-if="isLeftExpanded" class="expanded-content">
      <div class="search-container">
        <input class="search-bar" type="text" placeholder="Search..." />
        <select class="dropdown">
          <option value="id">ID/URI</option>
          <option value="rdf">RDF Label</option>
        </select>
      </div>

      <div class="toggles-and-levels">
        <label class="toggle-label"> <input type="checkbox" /> Show Deprecated </label>
        <label class="toggle-label"> <input type="checkbox" /> View Labels in Graph </label>

        <div class="levels-inputs">
          <div class="input-group">
            <label class="level-label">Levels Above:</label>
            <input type="number" min="0" max="6" class="small-input" value="0" />
          </div>
          <div class="input-group">
            <label class="level-label">Levels Below:</label>
            <input type="number" min="0" max="6" class="small-input" value="0" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.left-sidepanel {
  display: flex;
  flex-direction: column;
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
  overflow: hidden;
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

.expanded-content {
  overflow: hidden;
}

.search-container {
  display: flex;
  flex-direction: column;
  margin: 1rem;
  margin-top: 3rem;
}

.search-bar {
  width: 100%;
  padding: 0.5rem;
  margin-bottom: 0.5rem;
  max-width: 220px;
  border: 1px solid white;
  background-color: white;
  color: var(--color-nav-background);
}

.dropdown {
  width: 100%;
  padding: 0.5rem;
  max-width: 220px;
  border: 1px solid white;
  background-color: white;
  margin-bottom: 30px;
  color: var(--color-nav-background);
}

.toggles-and-levels {
  margin: 1rem;
  margin-bottom: 20px;
}

.toggle-label {
  display: flex;
  align-items: center;
  color: white;
  margin-bottom: 10px;
  white-space: nowrap;
}

.toggle-label input[type='checkbox'] {
  margin-right: 10px;
}

.levels-inputs {
  margin-top: 3rem;
  display: flex;
  justify-content: space-between;
}

.input-group {
  display: flex;
  flex-direction: column;
  width: 40%;
}

.level-label {
  color: white;
  white-space: nowrap;
}

.small-input {
  width: 100%;
  padding: 0.25rem;
  background-color: white;
  color: var(--color-nav-background);
  border: 1px solid white;
  text-align: center;
}
</style>
