<script setup lang="ts">
import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

const API_URL = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'
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

async function fetchChildren(node: any) {
  console.log(API_URL)
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return
  }
  try {
    const response = await fetch(`${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}`)
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
