<script setup lang="ts">
import GraphInfoSidepane from '../components/GraphInfoSidepane.vue'
import GraphSearchSidepane from '../components/GraphSearchSidepane.vue'
import GraphVisualisation from '../components/GraphVisualisation.vue'
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
