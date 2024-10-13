<script setup lang="ts">
import { breakpointsTailwind, useBreakpoints } from '@vueuse/core'
import { computed, ref, watch } from 'vue'

import { fetchNodeInfo } from '../assets/apiFunctions'
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// Mobile compatibility
const breakpoints = useBreakpoints(breakpointsTailwind)
const isSm = computed(() => breakpoints.smaller('sm').value)

// State variables
const showDeprecated = ref(false)
const showLabels = ref(true)
// The ID of the selected node for which we are rendering the graph - default is `Thing`
const selectedNodeId = ref('http://data.15926.org/dm/Thing')

// Side panel state
const isLeftExpanded = ref(false)
const isRightExpanded = ref(false)

// node spacing
const nodeDistanceX = ref(30)
const nodeDistanceY = ref(600)

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
 * Fetches the node information and updates the right side panel if the label is different.
 * Closes the right side panel if the same label is clicked again.
 * @param {string} nodeUri - The URI of the node for which the label was clicked.
 */
async function handleLabelClicked(nodeUri: string) {
  let nodeInfo = await fetchNodeInfo(nodeUri)
  if (nodeInfo) {
    if (isRightExpanded.value && nodeInfoDisplay.value.label === nodeInfo.label) {
      // Close the right side panel if the same label is clicked again
      toggleIsRightExpanded()
    } else {
      // Update the node info display
      nodeInfoDisplay.value = {
        id: nodeInfo.id,
        label: nodeInfo.label,
        definition: nodeInfo.definition,
        deprecation: nodeInfo.deprecation,
        parents: nodeInfo.parents,
        types: nodeInfo.types
      }
      // Open the right side panel if it isn't open
      if (!isRightExpanded.value) {
        toggleIsRightExpanded()
      }
    }
  }
}

// watch for changes in the isSm computed property and implement the logic to only allow one side panel to be expanded at a time
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

/**
 * Toggles the left side panel expanded state.
 */
function toggleIsLeftExpanded() {
  if (isSm.value && isRightExpanded.value) {
    isRightExpanded.value = false
  }
  isLeftExpanded.value = !isLeftExpanded.value
}

/**
 * Toggles the right side panel expanded state.
 */
function toggleIsRightExpanded() {
  if (isSm.value && isLeftExpanded.value) {
    isLeftExpanded.value = false
  }
  isRightExpanded.value = !isRightExpanded.value
}
</script>

<template>
  <div>
    <GraphSearchSidepane
      @node-selected="handleNodeSelected"
      @toggle-deprecated="handleToggleDeprecated"
      :is-left-expanded="isLeftExpanded"
      @toggle-is-left-expanded="toggleIsLeftExpanded"
      @toggle-labels="handleToggleLabels"
    />
    <GraphInfoSidepane
      :node-info-display="nodeInfoDisplay"
      :is-right-expanded="isRightExpanded"
      @toggle-is-right-expanded="toggleIsRightExpanded"
    />
    <GraphVisualisation
      :include-deprecated="showDeprecated"
      :selected-node-id="selectedNodeId"
      @label-clicked="handleLabelClicked"
      :show-labels="showLabels"
      :node-distance-x="nodeDistanceX"
      :node-distance-y="nodeDistanceY"
    />
  </div>
</template>

<style scoped></style>
