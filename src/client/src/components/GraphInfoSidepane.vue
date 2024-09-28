<script setup lang="ts">
import { ref, watch } from 'vue'

const props = defineProps({
  nodeUri: {
    type: String,
    required: true
  }
})

const isRightExpanded = ref(false)
const rdfData = ref(null)
const loading = ref(false)
const apiUrl = 'http://localhost:5000'

function toggleRightNav(): void {
  isRightExpanded.value = !isRightExpanded.value
}

defineExpose({
  toggleRightNav
})

async function fetchNodeData(): Promise<void> {
  loading.value = true
  try {
    const endpoint = `/node/info/${encodeURIComponent(props.nodeUri)}`
    const response = await fetch(`${apiUrl}${endpoint}`)

    if (!response.ok) {
      throw new Error(`Failed to fetch node data: ${response.statusText}`)
    }

    const data = await response.json()
    rdfData.value = data
  } catch (error) {
    console.error('Error fetching node data:', error)
    rdfData.value = null
  } finally {
    loading.value = false
  }
}

watch(() => props.nodeUri, fetchNodeData, { immediate: true })
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
          <!-- If data is loading, show loading state -->
          <div v-if="loading">Loading data...</div>

          <!-- If RDF data exists, display RDF information -->
          <div v-if="rdfData && !loading">
            <pre>{{ rdfData }}</pre>
            <!-- For debugging -->
            <div v-for="(value, key) in rdfData" :key="key" class="rdf-field">
              <strong class="rdf-field-name">{{ key }}:</strong>
              <span class="rdf-field-value">{{ formatValue(value) }}</span>
            </div>
          </div>

          <!-- If no data and not loading, show no data message -->
          <div v-else-if="!loading && !rdfData">No data available.</div>
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
  overflow: hidden; /* Ensure the sidebar itself doesn't scroll */
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
