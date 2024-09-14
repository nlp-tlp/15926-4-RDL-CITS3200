<script setup lang="ts">
import axios from 'axios'
import { onMounted, ref } from 'vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

// const data = ref({
//   name: 'root',
//   children: [
//     {
//       name: 'child1',
//       children: [
//         {
//           name: 'child1.1',
//           children: [
//             {
//               name: 'child1.1.1',
//               children: [],
//               extra_parents: [{ name: 'child1.2' }]
//             }
//           ]
//         },
//         {
//           name: 'child1.2',
//           children: []
//         }
//       ]
//     },
//     {
//       name: 'child2',
//       children: []
//     }
//   ]
// })

const data = ref({})
const depth = ref(2) // Specify the depth up to which the graph should be fetched

onMounted(() => {
  fetchGraphData()
})

async function fetchGraphData() {
  try {
    const rootResponse = await axios.get('http://127.0.0.1:5000/graph/root')
    const rootNode = rootResponse.data

    // Fetch children recursively up to the specified depth
    await fetchChildrenRecursively(rootNode, 0, depth.value)

    data.value = rootNode
    console.log(data.value)

    // Call the countNestedObjects function after the data has been fetched
    console.log(countNestedObjects(data.value))
  } catch (error) {
    console.error(error)
  }
}

async function fetchChildrenRecursively(node: any, currentDepth: number, maxDepth: number) {
  if (currentDepth >= maxDepth) {
    return
  }

  try {
    const childrenResponse = await axios.get(
      `http://127.0.0.1:5000/node/children/${encodeURIComponent(node.id)}`
    )
    const children = childrenResponse.data.children

    node.children = children

    // Fetch children for each child node recursively
    for (const child of children) {
      await fetchChildrenRecursively(child, currentDepth + 1, maxDepth)
    }
  } catch (error) {
    console.error(error)
  }
}

function countNestedObjects(node: any): number {
  if (!node || !node.children) {
    return 1
  }

  let count = 1 // Start by counting the current node

  for (const child of node.children) {
    count += countNestedObjects(child) // Recursively count the children
  }

  return count
}
</script>

<template>
  <div class="container">
    <h1>Graph</h1>
    <GraphSearchSidepane />
    <GraphInfoSidepane />

    <!-- Ensure data is passed correctly -->
    <GraphVisualisation :data="data" />
  </div>
</template>

<style scoped>
.container {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
