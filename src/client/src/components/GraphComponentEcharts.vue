<template>
  <div id="chart-container" ref="chartContainer">
    <div ref="chart" style="width: 100%; height: 100%"></div>
  </div>
</template>

<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted, ref } from 'vue'

const chartContainer = ref(null)
const chart = ref<echarts.EChartsType | null>(null)

const nodes: { id: string; name: string; level: number; x?: number; y?: number }[] = [
  { id: '1', name: 'Parent', level: 0 },
  { id: '2', name: 'Child 1', level: 1 },
  { id: '3', name: 'Child 2', level: 1 },
  { id: '4', name: 'Grandchild 1', level: 2 },
  { id: '5', name: 'Grandchild 2', level: 2 },
  { id: '6', name: 'Child 3', level: 1 },
  { id: '7', name: 'Grandchild 3', level: 2 },
  { id: '8', name: 'Grandchild 4', level: 2 },
  { id: '9', name: 'Child 4', level: 1 },
  { id: '10', name: 'Grandchild 5', level: 2 },
  { id: '11', name: 'Grandchild 6', level: 2 },
  { id: '12', name: 'Grandchild 7', level: 2 },
  { id: '13', name: 'Greatgrandchild 1', level: 3 },
  { id: '14', name: 'Parent 2', level: 0 }
]

const edges = [
  { source: '2', target: '1' },
  { source: '3', target: '1' },
  { source: '4', target: '2' },
  { source: '5', target: '2' },
  { source: '6', target: '1' },
  { source: '7', target: '3' },
  { source: '8', target: '3' },
  { source: '8', target: '2' },
  { source: '9', target: '14' },
  { source: '10', target: '9' },
  { source: '11', target: '3' },
  { source: '12', target: '9' },
  { source: '13', target: '7' }
]

const layoutHierarchy = () => {
  const levelWidth = 200
  const levelHeight = 100
  const levels: any[] = []

  nodes.forEach((node: { y?: number; id: string; name: string; level: number; x?: number }) => {
    const level = node.level
    const siblings = levels[level] || []
    node.x = level * levelWidth

    // Position the node in the center if it has no siblings
    node.y = siblings.length
      ? siblings.reduce((sum: any, sibling: { y: any }) => sum + sibling.y, 0) / siblings.length +
        levelHeight
      : 0

    // Adjust the vertical position to avoid overlapping with siblings
    siblings.push(node)
    levels[level] = siblings
  })

  // Apply "gravity" to cluster children vertically closer to their parents
  edges.forEach(({ source, target }) => {
    const parentNode = nodes.find((n) => n.id === source)
    const childNode = nodes.find((n) => n.id === target)

    if (!parentNode || !childNode) {
      return
    }

    // Cluster child nodes around their parent's y-position
    const spread = levelHeight * (Math.random() - 0.5)
    childNode.y = parentNode.y !== undefined ? parentNode.y + spread : 0
  })
}

onMounted(() => {
  chart.value = echarts.init(chartContainer.value)

  layoutHierarchy()

  const option = {
    tooltip: {},
    series: [
      {
        type: 'graph',
        layout: 'none',
        data: nodes.map((node) => ({
          id: node.id,
          name: node.name,
          x: node.x,
          y: node.y
        })),
        edges,
        roam: true, // Enable panning and zooming
        label: {
          show: true,
          position: 'right'
        },
        lineStyle: {
          curveness: 0 // Slightly curved edges
        },
        edgeSymbol: ['none', 'arrow'],
        edgeSymbolSize: [4, 10],
        emphasis: {
          focus: 'adjacency'
        }
      }
    ]
  }

  chart.value.setOption(option)

  window.addEventListener('resize', () => {
    chart.value?.resize()
  })
})
</script>

<style scoped>
#chart-container {
  width: 100lh;
  height: 100vh; /* Full screen height */
}
</style>
