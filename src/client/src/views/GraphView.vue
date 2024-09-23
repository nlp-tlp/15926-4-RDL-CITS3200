<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// API endpoint
const API_URL = 'http://127.0.0.1:5000'

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

async function fetchChildren(node: any) {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return
  }
  try {
    const response = await axios.get(`${API_URL}/node/children/${encodeURIComponent(node.id)}`)
    if (response && response.data && Array.isArray(response.data.children)) {
      // update the children of the node
      node.children = response.data.children
      // update the data object
      data.value = { ...data.value }
    } else {
      console.error('Invalid response:', response)
    }
  } catch (error: any) {
    if (error.response) {
      // Server responded with a status other than 2xx
      console.error('Server error:', error.response.status, error.response.data)
    } else if (error.request) {
      // Request was made but no response received
      console.error('Network error:', error.request)
    } else {
      // Something else happened
      console.error('Error:', error.message)
    }
  }
}
</script>

<template>
  <div class="container">
    <GraphSearchSidepane />
    <GraphInfoSidepane />
    <GraphVisualisation :data="data" :fetch-children="fetchChildren" />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
