<script setup lang="ts">
import axios from 'axios'
import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// Initial data for the root of the graph
const data = ref({
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
  children: []
})

async function fetchChildren(node: any) {
  try {
    const childrenResponse = await axios.get(
      `http://127.0.0.1:5000/node/children/${encodeURIComponent(node.id)}`
    )
    const children = childrenResponse.data.children
    node.children = children

    // Trigger reactivity
    data.value = { ...data.value }
  } catch (error) {
    console.error('Failed to fetch children:', error)
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
