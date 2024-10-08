<script setup lang="ts">
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import { computed, ref, watch } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

const breakpoints = useBreakpoints(breakpointsTailwind)

const isSm = computed(() => breakpoints.smaller('sm').value)

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

const showDeprecated = ref(false)

async function fetchChildren(node: any) {
  console.log(API_URL)
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

const theNodeInfoDisplay = {
  ID: '',
  Label: '',
  Definition: '',
  Dep: '',
  Parents: '',
  Types: ''
}

const nodeInfoDisplay = ref(theNodeInfoDisplay)
const infoTag = '/node/info/'

const isLeftExpanded = ref(false)
const isRightExpanded = ref(false)

watch(
  isSm,
  () => {
    isLeftExpanded.value = false
    isRightExpanded.value = false
  },
  {
    immediate: true
  }
)

function toggleIsLeftExpanded() {
  if (isSm.value && isRightExpanded.value) return
  isLeftExpanded.value = !isLeftExpanded.value
}

function toggleIsRightExpanded() {
  if (isSm.value && isLeftExpanded.value) return
  isRightExpanded.value = !isRightExpanded.value
}

async function fetchNodeInfo(nodeId: string) {
  try {
    const response = await fetch(`${API_URL}${infoTag}${encodeURIComponent(nodeId)}`)
    if (!response.ok) {
      console.error('Failed to fetch node info:', response.status)
      return null
    }
    const nodeInfo = await response.json()
    nodeInfoDisplay.value.Label = nodeInfo.label
    nodeInfoDisplay.value.Definition = nodeInfo.definition
    if (nodeInfo.dep === null) {
      nodeInfoDisplay.value.Dep = 'N/A'
    } else {
      nodeInfoDisplay.value.Dep = nodeInfo.dep
    }
    nodeInfoDisplay.value.ID = nodeInfo.id
    nodeInfoDisplay.value.Parents = ''
    for (let i = 0; i < nodeInfo.parents.length; i++) {
      nodeInfoDisplay.value.Parents += '• ' + nodeInfo.parents[i] + '\n'
    }
    nodeInfoDisplay.value.Types = ''
    for (let i = 0; i < nodeInfo.types.length; i++) {
      nodeInfoDisplay.value.Types += '• ' + nodeInfo.types[i] + '\n'
    }

    return {
      nodeInfoDisplay
    }
  } catch (error) {
    console.error('Error fetching node info:', error)
    return null
  }
}

async function handleLabelClicked(nodeUri: string) {
  await fetchNodeInfo(nodeUri)
  if (isSm.value && isLeftExpanded.value) {
    isLeftExpanded.value = false
    //on small screens, only allow one sidepanel open at a time
  }
  isRightExpanded.value = true
  infoPaneRef.value.toggleRightNav()
}

const infoPaneRef = ref()

// Toggles "showDeprecated" and re-fetches the node's children.
function handleShowDeprecatedToggle(value: boolean) {
  showDeprecated.value = value
  if (data.value && data.value.id) {
    fetchChildren(data.value)
  }
}

const showLabelsInGraph = ref(true)

// Toggles whether labels are displayed in the graph.
function handleToggleLabels(value: boolean) {
  showLabelsInGraph.value = value
}
</script>

<template>
  <div class="container">
    <GraphSearchSidepane
      :is-left-expanded="isLeftExpanded"
      @toggle-is-left-expanded="toggleIsLeftExpanded"
      @toggle-labels="handleToggleLabels"
      @toggle-deprecated="handleShowDeprecatedToggle"
    />
    <GraphInfoSidepane
      ref="infoPaneRef"
      :node-info-display="nodeInfoDisplay"
      :is-right-expanded="isRightExpanded"
      @toggle-is-right-expanded="toggleIsRightExpanded"
    />
    <GraphVisualisation
      :data="data"
      :fetch-children="fetchChildren"
      @label-clicked="handleLabelClicked"
      :show-labels="showLabelsInGraph"
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
