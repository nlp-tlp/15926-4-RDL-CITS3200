<script setup lang="ts">
import GraphComponentD3 from '../components/GraphComponentD3.vue'
import GraphComponentEcharts from '../components/GraphComponentEcharts.vue'
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
</script>

<template>
  <div>
    <h2>Graph</h2>
    <GraphSearchSidepane />
    <GraphInfoSidepane />
    <!-- <GraphComponentEcharts /> -->
    <GraphComponentD3 />
  </div>
</template>

<style scoped></style>
