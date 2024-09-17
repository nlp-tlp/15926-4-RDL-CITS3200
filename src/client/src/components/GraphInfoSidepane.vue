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

const isRightExpanded = ref(props.initialExpanded)

// Reactive object to hold RDF data
const rdfData = ref<Record<string, any> | null>(null)

// Function to toggle the side panel
function toggleRightNav(): void {
  isRightExpanded.value = !isRightExpanded.value
}

// Function to fetch node data from the API
async function fetchNodeData(nodeUri: string) {
  try {
    const response = await fetch(`http://localhost:5000/node/info/${encodeURIComponent(nodeUri)}`)
    if (!response.ok) {
      throw new Error("Failed to fetch data")
    }
    rdfData.value = await response.json()
  } catch (error) {
    console.error("Failed to fetch node data:", error)
  }
}

// Expose this function to be called from parent component when a node is selected
defineExpose({
  onNodeSelect(nodeUri: string) {
    fetchNodeData(nodeUri)
  }
})
</script>

<script lang="ts">
/**
 * GraphInfoSidepane component represents the expandable side panel containing RDF information functionality.
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
  <div>
    <button class="right-btn" @click="toggleRightNav" :class="{ 'expanded-btn': isRightExpanded }">
      &#9776;
    </button>

    <transition name="sidepanel">
      <div v-if="isRightExpanded" class="right-sidepanel">
        <p class="right-text">Graph Information</p>

        <div class="rdf-info">
          <!-- Render RDF data if it exists -->
          <div v-if="rdfData">
            <div v-for="(value, key) in rdfData" :key="key" class="rdf-field">
              <strong class="rdf-field-name">{{ key }}:</strong>
              <span class="rdf-field-value">
                <slot :name="key" :value="value">
                  {{ value }}
                </slot>
              </span>
            </div>
          </div>
          <div v-else>
            <p>Loading data...</p>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.right-btn {
  position: fixed;
  top: 5rem;
  right: 0.5rem;
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

.right-sidepanel {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  padding-top: 0.25rem;
  height: calc(100vh - var(--navbar-height, 4.5rem));
  width: 250px;
  position: fixed;
  z-index: 1;
  top: var(--navbar-height, 4.5rem);
  right: 0;
  background-color: var(--color-nav-background);
  transition:
    transform 0.5s ease,
    background-color 0.5s ease;
  transform: translateX(0);
  overflow: hidden; /* Ensure the side panel itself does not scroll */
}

.right-text {
  margin: 0.75rem 0 0 1rem;
  color: white;
  white-space: nowrap;
}

.sidepanel-enter-active,
.sidepanel-leave-active {
  transition: all 0.5s ease;
}

.sidepanel-enter-from,
.sidepanel-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.rdf-info {
  flex: 1; /* Allow rdf-info to take up remaining space */
  margin: 1rem;
  color: white;
  overflow-y: auto;
  overflow-x: hidden;
  -ms-overflow-style: none; /* IE and Edge */
  scrollbar-width: none; /* Firefox */
}

.rdf-info::-webkit-scrollbar {
  display: none; /* Chrome, Safari, Opera */
}

.rdf-field {
  margin-bottom: 1rem;
}

.rdf-field-name {
  display: block;
  font-weight: bold;
}

.rdf-field-value {
  display: block;
  margin-left: 1rem;
  white-space: normal;
  word-wrap: break-word;
}
</style>
