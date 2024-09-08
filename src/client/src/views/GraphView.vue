<template>
  <div>
    <h2>Graph</h2>
    <GraphSearchSidepane />
    <GraphInfoSidepane />
    <!-- <GraphComponentEcharts /> -->
    <GraphVisualisation :data />
  </div>
</template>

<script setup lang="ts">
import GraphVisualisation from '@/components/GraphVisualisation.vue'

import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import { data } from './data'

// const data = generateBinaryTree(13)

// function generateBinaryTree(depth) {
//   let idCounter = 1

//   function addChildren(node, level) {
//     if (level >= depth) return

//     const children = []
//     // Randomly vary number of children on the last level
//     const isLastLevel = level === depth - 1
//     const childCount = isLastLevel ? (Math.random() > 0.5 ? 2 : 1) : 2

//     for (let i = 0; i < childCount; i++) {
//       const newNode = {
//         id: ++idCounter,
//         name: `Node ${idCounter}`,
//         x: level * 100,
//         y: level * 50 + i * 15, // Ensure minimum 15px spacing between nodes
//         children: []
//       }
//       children.push(newNode)
//     }

//     node.children = children

//     // Recursively add children
//     children.forEach((child) => addChildren(child, level + 1))
//   }

//   const root = { id: 1, name: 'Root', x: 0, y: 0, children: [] }
//   addChildren(root, 1)
//   return root
// }

function countNestedObjects(node: any): number {
  let count = 1 // Start by counting the current node

  if (node.children && node.children.length > 0) {
    for (const child of node.children) {
      count += countNestedObjects(child) // Recursively count the children
    }
  }

  return count
}

console.log(countNestedObjects(data))
</script>
