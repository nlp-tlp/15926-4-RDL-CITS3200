<script setup lang="ts">
import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// API URL
const API_URL = 'http://127.0.0.1:5000'
const childrenEndpoint = '/node/children/'

// initial data for the root of the graph
const initialData = {
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
  deprecation: null,
  // Thing starts with expanded set to true so as not to re-call the expansion (in toggleCollapse) once the children are fetched
  expanded: true
}
// make the data reactive
const data = ref(initialData)

// reactive property for "Show Deprecated" functionality
const showDeprecated = ref(false)

async function fetchChildren(node: any) {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return
  }
  try {
    const dep = String(showDeprecated.value)
    const url = `${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}?dep=${dep}`
    const response = await fetch(url)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return
    }
    const responseData = await response.json()
    if (responseData && Array.isArray(responseData.children)) {
      // update the children of the node
      node.children = responseData.children
      // update the data object
      data.value = { ...data.value }
    } else {
      console.error('Invalid response:', responseData)
    }
  } catch (error: any) {
    if (error instanceof TypeError) {
      // Network error or other fetch-related error
      console.error('Network error:', error.message)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
  }
}

// Toggles "showDeprecated" and re-fetches the node's children.
function handleShowDeprecatedToggle (value: boolean) {
  showDeprecated.value = value
  if (data.value && data.value.id) {
    fetchChildren(data.value);
  }
}

// reactive property for "View Labels in Graph"
const showLabelsInGraph = ref(true)

// Toggles whether labels are displayed in the graph.
function handleToggleLabels (value: boolean) {
  showLabelsInGraph.value = value
}

</script>

<template>
  <div class="container">
    <GraphSearchSidepane @toggle-labels="handleToggleLabels" @toggle-deprecated="handleShowDeprecatedToggle" />
    <GraphInfoSidepane />
    <GraphVisualisation :data="data" :fetch-children="fetchChildren" :show-labels="showLabelsInGraph" />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
