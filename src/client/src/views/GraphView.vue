<script setup lang="ts">
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'

const data = {
  name: 'root',
  children: [
    {
      name: 'child1',
      children: [
        {
          name: 'child1.1',
          children: [
            {
              name: 'child1.1.1',
              children: []
            },
            {
              name: 'child1.1.2',
              children: []
            }
          ]
        },
        {
          name: 'child1.2',
          children: []
        }
      ]
    },
    {
      name: 'child2',
      children: [
        {
          name: 'child2.1',
          children: []
        },
        {
          name: 'child2.2',
          children: [],
          extra_parents: [{ name: 'child1' }, { name: 'root' }]
        }
      ]
    }
  ]
}

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

<template>
  <div class="container">
    <h1>Graph</h1>
    <GraphSearchSidepane />
    <GraphInfoSidepane />

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
