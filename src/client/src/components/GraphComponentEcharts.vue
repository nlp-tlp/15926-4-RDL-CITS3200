<template>
  <div style="overflow: auto">
    <div ref="chartContainer" style="min-height: 2000px; min-width: 1200px"></div>
  </div>
</template>

<script lang="ts">
import * as echarts from 'echarts'
import { defineComponent, onMounted, ref } from 'vue'

export default defineComponent({
  name: 'EChartsTree',
  setup() {
    const chartContainer = ref<HTMLElement | null>(null)

    // Generates a large binary tree dataset with a specified depth.
    const generateBinaryTree = (depth: number): any => {
      let idCounter = 1

      const addChildren = (node: any, level: number) => {
        if (level >= depth) return

        const children: any[] = []
        const isLastLevel = level === depth - 1
        const childCount = isLastLevel ? (Math.random() > 0.5 ? 2 : 1) : 2

        for (let i = 0; i < childCount; i++) {
          const newNode = {
            id: ++idCounter,
            name: `Node ${idCounter}`,
            x: level * 100,
            y: level * 50 + i * 15, // Ensure minimum 15px spacing between nodes
            children: []
          }
          children.push(newNode)
        }

        node.children = children
        children.forEach((child) => addChildren(child, level + 1))
      }

      const root = { id: 1, name: 'Root', x: 0, y: 0, children: [] }
      addChildren(root, 1)
      return root
    }

    // Initialize the chart after the component is mounted
    const initChart = () => {
      if (chartContainer.value) {
        const chart = echarts.init(chartContainer.value)

        const option = {
          tooltip: {},
          series: [
            {
              type: 'tree',
              data: [generateBinaryTree(15)], // 15 levels deep binary tree
              layout: 'orthogonal',
              orient: 'LR', // Left to Right
              left: '2%',
              right: '2%',
              top: '15px',
              bottom: '15px',
              symbol: 'circle',
              symbolSize: 8,
              label: {
                position: 'right',
                verticalAlign: 'middle',
                align: 'left',
                fontSize: 10
              },
              lineStyle: {
                curveness: 0.4 // Adjust Bezier curves
              },
              expandAndCollapse: false, // Everything is expanded
              animationDuration: 550,
              animationDurationUpdate: 750,
              // animation: false,
              roam: true, // Enable panning and zooming
              labelLayout: {
                hideOverlap: true
              },
              edgeShape: 'curve'
            }
          ]
        }

        chart.setOption(option)

        // Resize chart on window resize
        window.addEventListener('resize', () => {
          chart.resize()
        })
      }
    }

    // Hook to mount the chart
    onMounted(() => {
      initChart()
    })

    return {
      chartContainer
    }
  }
})
</script>

<style scoped>
/* Ensure container takes up full width and height */
html,
body {
  margin: 0;
  padding: 0;
  /* width: 100vw;
  height: 100vh; */
  overflow: hidden; /* Hide overflow if container grows large */
}

#chart-container {
  /* width: 100vw;
  height: 100vh; */
  position: relative;
}
</style>
