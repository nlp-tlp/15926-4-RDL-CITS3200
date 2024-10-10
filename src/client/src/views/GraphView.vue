<script setup lang="ts">
import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// Boolean flag to include deprecated nodes in the graph - default is false
const showDeprecated = ref(false)
// Boolean flag to show labels on the graph nodes - default is true
const showLabels = ref(true)
// The ID of the selected node for which we are rendering the graph - default is `Thing`
const selectedNodeId = ref('http://data.15926.org/dm/Thing')

function handleToggleDeprecated(val: boolean) {
  showDeprecated.value = val
}

function handleNodeSelected(nodeId: string) {
  selectedNodeId.value = nodeId
}

function handleToggleLabels(val: boolean) {
  showLabels.value = val
}
</script>

<template>
  <div class="container">
    <GraphSearchSidepane
      @node-selected="handleNodeSelected"
      @toggle-deprecated="handleToggleDeprecated"
      @toggle-labels="handleToggleLabels"
    />
    <GraphInfoSidepane />
    <GraphVisualisation
      :include-deprecated="showDeprecated"
      :selected-node-id="selectedNodeId"
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
