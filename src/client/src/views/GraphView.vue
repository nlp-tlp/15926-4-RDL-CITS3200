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

async function fetchChildren(node: any) {
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

const nodeInfoDisplay = {
  label: 'Thing',
  definition: 'Thing is anything',
  dep: 'null',
  id: 'http://data.15926.org/dm/Thing',
  parents: '[]',
  properties: { 'http://data.15926.org/meta/valEffectiveDate': ['2023-01-15Z'] },
  types: ['http://data.15926.org/rdl/RDS2226571', 'http://www.w3.org/2002/07/owl#Class']
}

// const nodeinfo = ref(null)
const infoTag = '/node/info/'

async function fetchNodeInfo(nodeId: string) {
  try {
    const response = await fetch(`${API_URL}${infoTag}${encodeURIComponent(nodeId)}`)
    if (!response.ok) {
      console.error('Failed to fetch node info:', response.status)
      return null
    }
    const nodeInfo = await response.json()
    console.log('Definition is:', nodeInfo.definition)
    console.log('id is:', nodeInfo.id)
    console.log('dep is:', nodeInfo.dep)

    nodeInfoDisplay.label = nodeInfo.label
    nodeInfoDisplay.definition = nodeInfo.definition
    nodeInfoDisplay.dep = nodeInfo.dep
    nodeInfoDisplay.id = nodeInfo.id
    nodeInfoDisplay.parents = nodeInfo.parents
    nodeInfoDisplay.properties = nodeInfo.properties
    nodeInfoDisplay.types = nodeInfo.types

    // Ensure the data has the correct structure before returning it
    return {
      nodeInfoDisplay
    }
  } catch (error) {
    console.error('Error fetching node info:', error)
    return null
  }
}

function handleNodeClicked(nodeUri: string) {
  fetchNodeInfo(nodeUri)
}
</script>

<template>
  <div class="container">
    <GraphSearchSidepane />
    <GraphInfoSidepane :node-info-display="nodeInfoDisplay" />
    <GraphVisualisation
      :data="data"
      :fetch-children="fetchChildren"
      @node-clicked="handleNodeClicked"
    />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
