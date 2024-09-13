<script setup lang="ts">
import { ref } from 'vue'

const props = withDefaults(
  defineProps<{
    initialExpanded?: boolean
  }>(),
  {
    initialExpanded: false
  }
)

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
  <button class="left-btn" @click="toggleLeftNav" :class="{ 'expanded-btn': isLeftExpanded }">
    &#9776;
  </button>

  <transition name="sidepanel">
    <div v-if="isLeftExpanded" class="left-sidepanel">
      <p class="left-text">Graph Search</p>

      <div v-if="isLeftExpanded" class="expanded-content">
        <div class="search-container">
          <div class="search-wrapper">
            <svg
              class="search-icon"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 24 24"
              width="24"
              height="24"
            >
              <path
                d="M23 21l-5.5-5.5a9.5 9.5 0 1 0-1.4 1.4L21 22.4a1 1 0 0 0 1.4-1.4zM10 18a8 8 0 1 1 8-8 8 8 0 0 1-8 8z"
              />
            </svg>
            <input class="search-bar" type="text" placeholder="Search..." />
          </div>
          <select class="dropdown">
            <option value="id">ID/URI</option>
            <option value="rdf">RDF Label</option>
          </select>
        </div>

        <div v-if="isLeftExpanded" class="toggles-and-levels">
          <label class="toggle-label"> <input type="checkbox" /> Show Deprecated </label>
          <label class="toggle-label"> <input type="checkbox" /> View Labels in Graph </label>

          <div v-if="isLeftExpanded" class="levels-inputs">
            <div class="input-group">
              <label class="level-label">Levels Above:</label>
              <input type="number" min="0" max="6" class="small-input" value="0" />
            </div>
            <div v-if="isLeftExpanded" class="input-group">
              <label class="level-label">Levels Below:</label>
              <input type="number" min="0" max="6" class="small-input" value="0" />
            </div>
          </div>
        </div>
        <button class="search-btn">Submit</button>
      </div>
    </div>
  </transition>
</template>

<style scoped>
.left-btn {
  position: fixed;
  top: 5rem;
  left: 0.5rem;
  background-color: transparent;
  cursor: pointer;
  border: none;
  font-size: 22px;
  font-weight: bold;
  z-index: 2; /* Ensure the button is always on top */
  color: var(--color-nav-background);
  transition: color 0.5s ease;
}

.expanded-btn {
  color: white;
}

.left-sidepanel {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: 100%;
  width: 250px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  left: 0;
  background-color: var(--color-nav-background);
  transition:
    transform 0.5s ease,
    background-color 0.5s ease;
  transform: translateX(0);
}

.left-text {
  margin: 0.75rem 1rem 0 auto;
  color: white;
  white-space: nowrap;
}

.sidepanel-enter-active,
.sidepanel-leave-active {
  transition: all 0.5s ease;
}

.sidepanel-enter-from,
.sidepanel-leave-to {
  transform: translateX(-100%);
  opacity: 0;
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

.search-wrapper {
  position: relative;
}

.search-icon {
  position: absolute;
  left: 10px;
  top: 45%;
  transform: translateY(-50%);
  fill: white;
  transition: fill 0.3s;
}

.search-bar {
  width: 100%;
  padding: 1rem;
  padding-left: 50px;
  margin-bottom: 0.5rem;
  max-width: 220px;
  border: 1px solid white;
  background-color: var(--color-nav-background);
  color: white;
  border-radius: 8px;
  font-size: 1rem;
  transition:
    background-color 0.3s,
    color 0.3s;
}

.search-bar::placeholder {
  color: white;
}

.dropdown {
  width: 100%;
  padding: 0.75rem;
  max-width: 220px;
  border: 1px solid white;
  background-color: var(--color-nav-background);
  margin-bottom: 30px;
  color: white;
  border-radius: 8px;
  font-size: 1rem;
  cursor: pointer;
  transition:
    background-color 0.3s,
    border-color 0.3s;
}

.dropdown:focus {
  outline: none;
  border-color: var(--color-accent);
  background-color: var(--color-nav-background-dark);
}

.dropdown option {
  background-color: var(--color-nav-background);
  color: white;
}

.dropdown::-ms-expand {
  display: none;
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
  width: 45%;
}

.level-label {
  color: white;
  margin-bottom: 0.5rem;
  font-size: 0.875rem;
  font-weight: 500;
  white-space: nowrap;
}

.small-input {
  width: 100%;
  padding: 0.5rem;
  background-color: white;
  color: var(--color-nav-background);
  border: 1px solid white;
  border-radius: 8px;
  text-align: left;
  font-size: 0.875rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition:
    border-color 0.3s,
    box-shadow 0.3s;
  appearance: textfield;
}

.small-input::-webkit-inner-spin-button,
.small-input::-webkit-outer-spin-button {
  opacity: 1;
}

.small-input:focus {
  border-color: var(--color-nav-background);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
}

.search-btn {
  width: 80%;
  margin: 0 auto;
  padding: 0.75rem;
  background-color: var(--color-nav-background);
  color: white;
  margin-left: 20px;
  border: 2px solid white;
  border-radius: 8px;
  font-size: 0.875rem;
  font-weight: 800;
  cursor: pointer;
  margin-top: 20px;
  text-align: center;
  transition:
    background-color 0.3s,
    border-color 0.3s;
}
</style>
