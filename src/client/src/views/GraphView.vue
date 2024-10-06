<template>
  <div class="container">
    <GraphSearchSidepane
      @toggle-labels="handleToggleLabels"
      @toggle-deprecated="handleShowDeprecatedToggle"
    />
    <GraphInfoSidepane />
    <!-- <GraphVisualisation
      :data="childrensData"
      :fetch-children="fetchChildren"
      :show-labels="showLabelsInGraph"
    />
    <ReverseGraphVisualisation
      :data="parentsData"
      :fetch-children="fetchParents"
      :show-labels="showLabelsInGraph"
    /> -->
    <DoubleSidedGraphVisualisation
      :childrens-data="childrensData"
      :parents-data="parentsData"
      :fetch-children="fetchChildren"
      :fetch-parents="fetchParents"
      :show-labels="showLabelsInGraph"
    />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

import DoubleSidedGraphVisualisation from '@/components/DoubleSidedGraphVisualisation.vue'
import GraphInfoSidepane from '@/components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '@/components/GraphSearchSidepane.vue'
import GraphVisualisation from '@/components/GraphVisualisation.vue'
import ReverseGraphVisualisation from '@/components/ReverseGraphVisualisation.vue'

const API_URL = import.meta.env.VITE_SERVER_URL ?? 'http://127.0.0.1:5000'
const childrenEndpoint = '/node/children/'
const parentsEndpoint = '/node/children/' // TODO change to /node/parents/

// initial data for the root of the graph
const initialChildrenData = {
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
  deprecation: null,
  expanded: true
}
const initialParentsData = {
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
  deprecation: null,
  expanded: true
}
// make the data reactive
const childrensData = ref(initialChildrenData)
const parentsData = ref(initialParentsData)

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
      node.children = responseData.children
      childrensData.value = { ...childrensData.value }
    } else {
      console.error('Invalid response:', responseData)
    }
  } catch (error: any) {
    console.error('Error:', error.message)
  }
}

async function fetchParents(node: any) {
  if (!node || !node.id) {
    console.error('Invalid node:', node)
    return
  }
  try {
    const dep = String(showDeprecated.value)
    const url = `${API_URL}${parentsEndpoint}${encodeURIComponent(node.id)}?dep=${dep}`
    const response = await fetch(url)
    if (!response.ok) {
      console.error('Server error:', response.status, await response.text())
      return
    }
    const responseData = await response.json()
    if (responseData && Array.isArray(responseData.children)) {
      node.children = responseData.children // still marked as children for rendering purposes
      parentsData.value = { ...parentsData.value }
    } else {
      console.error('Invalid response:', responseData)
    }
  } catch (error: any) {
    console.error('Error:', error.message)
  }
}

// Toggles "showDeprecated" and re-fetches the node's children.
function handleShowDeprecatedToggle(value: boolean) {
  showDeprecated.value = value
  if (childrensData.value && childrensData.value.id) {
    fetchChildren(childrensData.value)
  }
  if (parentsData.value && parentsData.value.id) {
    fetchParents(parentsData.value)
  }
}

const showLabelsInGraph = ref(true)

// Toggles whether labels are displayed in the graph.
function handleToggleLabels(value: boolean) {
  showLabelsInGraph.value = value
}
</script>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* #graph1 {
  z-index: 1;
}

#graph2 {
  z-index: 0;
} */
</style>
