<template>
  <div id="main" style="width: 100vw; height: 100vh"></div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted } from 'vue'

import mockData from '../assets/mockData.json'

// Define the types for nodes and edges
interface Node {
  id: string
  name: string
  x: number
  y: number
  children?: Node[]
  _children?: Node[]
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
const colorScale = d3.scaleOrdinal(d3.schemeCategory10)

onMounted(() => {
  const { nodes, edges } = mockData as { nodes: Node[]; edges: Edge[] }

  const width = window.innerWidth
  const height = window.innerHeight

  const svg: d3.Selection<SVGSVGElement, unknown, HTMLElement, any> = d3
    .select('#main')
    .append('svg')
    .attr('width', width)
    .attr('height', height)
    .style('shape-rendering', 'geometricPrecision') // Ensure high-quality rendering
    .call(
      d3.zoom<SVGSVGElement, unknown>().on('zoom', (event) => {
        g.attr('transform', event.transform)
      })
    )

  const g: d3.Selection<SVGGElement, unknown, HTMLElement, any> = svg.append('g') // Append a group element to apply zoom and pan

  // Define arrow markers for directed edges
  g.append('defs')
    .append('marker')
    .attr('id', 'arrowhead')
    .attr('viewBox', '-0 -5 10 10')
    .attr('refX', 21) // Adjusted refX to position arrowheads correctly
    .attr('refY', 0)
    .attr('orient', 'auto')
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('xoverflow', 'visible')
    .append('svg:path')
    .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
    .attr('fill', '#000')
    .style('stroke', 'none')

  // Create a map of nodes by ID for easy lookup
  const nodeMap = new Map(nodes.map((node) => [node.id, node]))

  // Add children to nodes based on edges
  edges.forEach((edge) => {
    const parent = nodeMap.get(edge.target)
    const child = nodeMap.get(edge.source)
    if (parent && child) {
      if (!parent.children) {
        parent.children = []
      }
      parent.children.push(child)
    }
  })

  // Function to update the graph
  const update = (source: Node) => {
    // Flatten the nodes to include only visible nodes
    const visibleNodes: Node[] = []
    const traverse = (node: Node) => {
      visibleNodes.push(node)
      if (node.children) {
        node.children.forEach(traverse)
      }
    }
    traverse(source)

    // Create links with curved paths
    const link = g.selectAll('.link').data(
      edges.filter(
        (edge) =>
          visibleNodes.includes(nodeMap.get(edge.source)!) &&
          visibleNodes.includes(nodeMap.get(edge.target)!)
      ),
      (d: any) => d.source + '-' + d.target
    )

    link
      .enter()
      .append('path')
      .attr('class', 'link')
      .attr('stroke-width', 2)
      .attr('stroke', '#000')
      .attr('fill', 'none')
      .attr('marker-end', 'url(#arrowhead)')
      .attr('d', (d) => {
        const sourceNode = nodeMap.get(d.source)!
        const targetNode = nodeMap.get(d.target)!
        const dx = targetNode.x - sourceNode.x
        const dy = targetNode.y - sourceNode.y
        const dr = Math.sqrt(dx * dx + dy * dy) * 0.25 // Adjust the curvature
        return `M${sourceNode.x},${sourceNode.y}Q${(sourceNode.x + targetNode.x) / 2},${(sourceNode.y + targetNode.y) / 2 - dr},${targetNode.x},${targetNode.y}`
      })

    link.exit().remove()

    // Create nodes
    const node = g.selectAll('.node').data(visibleNodes, (d: any) => d.id)

    const nodeEnter = node
      .enter()
      .append('g')
      .attr('class', 'node')
      .attr('transform', (d) => `translate(${d.x},${d.y})`)
      .on('click', (event, d) => {
        if (d.children) {
          d._children = d.children
          d.children = undefined
        } else {
          d.children = d._children
          d._children = undefined
        }
        update(source)
      })

    nodeEnter
      .append('circle')
      .attr('r', 15)
      .attr('fill', (d) => colorScale(getNodeLevel(d.id).toString())) // Color nodes based on their level
      .attr('stroke', '#000') // Add a stroke to improve visual quality
      .attr('stroke-width', 1.5) // Increase stroke width for better quality

    nodeEnter.append('title').text((d) => d.name)

    const text = nodeEnter
      .append('text')
      .attr('dy', 3)
      .attr('x', 20)
      .style('text-anchor', 'start')
      .style('display', 'none') // Hide labels by default
      .text((d) => d.name)

    nodeEnter
      .on('mouseover', function () {
        d3.select(this).select('text').style('display', 'block')
      })
      .on('mouseout', function () {
        d3.select(this).select('text').style('display', 'none')
      })

    node.exit().remove()
  }

  // Initialize the graph with the root node
  const root = nodes.find((node) => node.id === 'Root')!
  update(root)
})
</script>

<script lang="ts">
export default {
  name: 'GraphComponentD3'
}
</script>

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
