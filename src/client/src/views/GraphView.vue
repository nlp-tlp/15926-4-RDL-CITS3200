<script setup lang="ts">
import { ref } from 'vue'

import { fetchNodeInfo } from '../assets/apiFunctions'
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// Boolean flag to include deprecated nodes in the graph - default is false
const showDeprecated = ref(false)
// Boolean flag to show labels on the graph nodes - default is true
const showLabels = ref(true)
// The ID of the selected node for which we are rendering the graph - default is `Thing`
const selectedNodeId = ref('http://data.15926.org/dm/Thing')

/**
 * Handles the event when the user toggles the deprecated nodes visibility.
 * @param {boolean} val - The new value of the flag to include deprecated nodes.
 */
function handleToggleDeprecated(val: boolean) {
  showDeprecated.value = val
}

/**
 * Handles the event when the user selects a node in the graph.
 * @param {string} nodeId - The ID of the selected node.
 */
function handleNodeSelected(nodeId: string) {
  selectedNodeId.value = nodeId
}

/**
 * Handles the event when the user toggles the visibility of labels on the graph nodes.
 * @param {boolean} val - The new value of the flag to show labels.
 */
function handleToggleLabels(val: boolean) {
  showLabels.value = val
}

const nodeInfoDisplay = ref({
  id: '',
  label: '',
  definition: '',
  deprecation: '',
  parents: '',
  types: ''
})

/**
 * Handles the event when a label is clicked on the graph.
 * @param {string} nodeUri - The URI of the node for which the label was clicked.
 */
async function handleLabelClicked(nodeUri: string) {
  let nodeInfo = await fetchNodeInfo(nodeUri)
  if (nodeInfo) {
    nodeInfoDisplay.value = {
      id: nodeInfo.id,
      label: nodeInfo.label,
      definition: nodeInfo.definition,
      deprecation: nodeInfo.deprecation,
      parents: nodeInfo.parents,
      types: nodeInfo.types
    }
    infoPaneRef.value.toggleRightNav()
  }
}
const infoPaneRef = ref()
</script>

<template>
  <div class="container">
    <GraphSearchSidepane
      @node-selected="handleNodeSelected"
      @toggle-deprecated="handleToggleDeprecated"
      @toggle-labels="handleToggleLabels"
    />
    <GraphInfoSidepane ref="infoPaneRef" :node-info-display="nodeInfoDisplay" />
    <GraphVisualisation
      :include-deprecated="showDeprecated"
      :selected-node-id="selectedNodeId"
      @label-clicked="handleLabelClicked"
      :show-labels="showLabels"
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
