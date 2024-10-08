<script setup lang="ts">
import { ref } from 'vue'

import GraphVisualisation from '../components/DoubleSidedGraphVisualisation.vue'
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'

const showDeprecated = ref(false)
const selectedNodeId = ref('')

function toggleShowDeprecated() {
  showDeprecated.value = !showDeprecated.value
  console.log('showDeprecated', showDeprecated.value)
}

function handleNodeSelected(nodeId: string) {
  selectedNodeId.value = nodeId
}
</script>

<template>
  <div class="container">
    <GraphSearchSidepane
      :show-deprecated="showDeprecated"
      @toggle-deprecated="toggleShowDeprecated"
      @node-selected="handleNodeSelected"
    />
    <GraphInfoSidepane />
    <GraphVisualisation :include-deprecated="showDeprecated" :selected-node-id="selectedNodeId" />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
