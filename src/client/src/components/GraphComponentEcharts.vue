<script setup lang="ts">
import * as echarts from 'echarts'
import { onMounted } from 'vue'

import mockData from '../assets/mockData.json'

// Define types for nodes and edges
interface Node {
  id: string
  name: string
  x: number
  y: number
  visible: boolean
  collapsed: boolean
  children: string[]
}

interface Edge {
  source: string
  target: string
}

// Function to get the level of a node from its ID
const getNodeLevel = (nodeId: string): number => {
  const match = nodeId.match(/Node(\d+)-\d+/)
  return match ? parseInt(match[1], 10) : 0
}

// Define a color scale for different levels
const colors = [
  '#1f77b4',
  '#ff7f0e',
  '#2ca02c',
  '#d62728',
  '#9467bd',
  '#8c564b',
  '#e377c2',
  '#7f7f7f',
  '#bcbd22',
  '#17becf'
]

// Function to toggle the visibility of child nodes recursively
const toggleChildren = (node: Node, nodes: Node[], edges: Edge[]) => {
  const toggleNodeVisibility = (node: Node, visible: boolean) => {
    node.children.forEach((childId) => {
      const childNode = nodes.find((n) => n.id === childId)
      if (childNode) {
        childNode.visible = visible
        if (!visible) {
          toggleNodeVisibility(childNode, visible)
        }
      }
    })
  }

  if (node.collapsed) {
    // Expand the node
    node.collapsed = false
    toggleNodeVisibility(node, true)
  } else {
    // Collapse the node
    node.collapsed = true
    toggleNodeVisibility(node, false)
  }
}

onMounted(() => {
  const chartDom = document.getElementById('main')!
  const myChart = echarts.init(chartDom, null, {
    renderer: 'svg'
  })
  let option: echarts.EChartsOption

  // Use the imported mock data
  const { nodes, edges } = mockData as { nodes: Node[]; edges: Edge[] }

  // Initialize nodes with visibility and collapsed state
  nodes.forEach((node) => {
    node.visible = true
    node.collapsed = false
    node.children = edges.filter((edge) => edge.source === node.id).map((edge) => edge.target)
  })

  const updateGraph = () => {
    option = {
      tooltip: {
        trigger: 'item',
        triggerOn: 'mousemove'
      },
      series: [
        {
          type: 'graph',
          layout: 'none',
          data: nodes
            .filter((node) => node.visible)
            .map((node) => ({
              id: node.id,
              name: node.name,
              x: node.x,
              y: node.y,
              symbolSize: 15,
              itemStyle: {
                color: colors[getNodeLevel(node.id) % colors.length] // Color nodes based on their level
              }
            })),
          links: edges
            .filter((edge) => {
              const sourceNode = nodes.find((node) => node.id === edge.source)
              const targetNode = nodes.find((node) => node.id === edge.target)
              return sourceNode?.visible && targetNode?.visible
            })
            .map((edge) => ({
              source: edge.source,
              target: edge.target,
              lineStyle: {
                type: 'solid',
                color: '#000',
                width: 2,
                curveness: 0.2
              },
              emphasis: {
                focus: 'adjacency'
              },
              symbol: ['none', 'arrow'],
              symbolSize: 10
            })),
          roam: true,
          label: {
            show: false, // Hide labels by default
            position: 'right'
          },
          emphasis: {
            label: {
              show: true // Show labels on hover
            }
          }
        }
      ]
    }

    myChart.setOption(option)
  }

  myChart.on('click', 'series.graph', (params: any) => {
    if (params.data) {
      const node = nodes.find((n) => n.id === params.data.id)
      if (node) {
        toggleChildren(node, nodes, edges)
        updateGraph()
      }
    }
  })

  updateGraph()
})
</script>

<script lang="ts">
export default {
  name: 'GraphComponentEcharts'
}
</script>

<template>
  <div id="main" style="width: 100vw; height: 100vh"></div>
</template>

<style scoped>
html,
body,
#app,
#main {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
