<script setup lang="ts">
import * as d3 from 'd3'
import { ref } from 'vue'

// Define the svgRef variable
const svgRef = ref<Element>()
</script>

<script lang="ts">
export default {
  name: 'GraphVisualisation'
}
</script>

<template>
  <div id="tree-container">
    <svg ref="svgRef"></svg>
  </div>
</template>

<style scoped></style>
