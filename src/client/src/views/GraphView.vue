<script setup lang="ts">
// import { ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// Initial data for the root of the graph
// const data = ref({
//   id: 'http://data.15926.org/dm/Thing',
//   label: 'Thing',
//   has_children: true,
//   deprecation: null,
//   children: []
// })

// async function fetchChildren(node: any) {
//   try {
//     const response = await fetch(`http://127.0.0.1:5000/node/children/${encodeURIComponent(node.id)}`)
//     if (!response.ok) {
//       throw new Error(`Failed to fetch children. Status: ${response.status}`)
//     }
//     const data = await response.json()
//     node.children = data.children

//     // Trigger reactivity
//     data.value = { ...data.value }
//   }
//   catch (error) {
//     console.error(error)
//   }
// }
</script>

<template>
  <div class="container">
    <GraphSearchSidepane />
    <GraphInfoSidepane />
    <GraphVisualisation />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
