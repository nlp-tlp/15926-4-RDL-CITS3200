<template>
  <div>
    <h2>Graph</h2>
    <GraphSearchSidepane />
    <GraphInfoSidepane />
    <GraphComponentEcharts />
    <!-- <GraphComponentD3 /> -->
  </div>
</template>

<script setup lang="ts">
// import GraphComponentD3 from '../components/GraphComponentD3.vue'
import GraphComponentEcharts from '../components/GraphComponentEcharts.vue'
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'

// const nodes = [
//   { id: '1', name: 'Root', category: 0 },
//   { id: '2', name: 'Child 1', category: 1 },
//   { id: '3', name: 'Child 2', category: 1 }
//   // More nodes...
// ]

// const edges = [
//   { source: '1', target: '2' },
//   { source: '1', target: '3' }
//   // More edges...
// ]
</script>

<style scoped></style>
