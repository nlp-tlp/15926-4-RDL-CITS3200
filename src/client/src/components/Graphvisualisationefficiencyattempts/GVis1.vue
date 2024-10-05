<script setup lang="ts">
import { test } from '@playwright/test'
import * as d3 from 'd3'
import { onMounted, ref, render, watch } from 'vue'

// API URL
const API_URL = 'http://127.0.0.1:5000'
const childrenEndpoint = '/node/children/'

// initial data for the global view
const globalRootNode = {
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
  dep: null,
  expanded: false
}

// initial data for the local view - to be passed in as prop in Graphview from Graphsearch
const localRootNode = {}

// reactive data object
const data = ref({})

// start with the global view
data.value = globalRootNode

// // fetch the children of a node from the server return a new node object with the children, if not return null
// async function fetchChildren(node: any) {
//   if (!node || !node.id) {
//     console.error('Invalid node:', node)
//     return null
//   }
//   // check if the node has children
//   if (!node.has_children) {
//     console.error('Node has no children:', node)
//     return null
//   }
//   try {
//     const response = await fetch(`${API_URL}${childrenEndpoint}${encodeURIComponent(node.id)}`)
//     if (!response.ok) {
//       console.error('Server error:', response.status, await response.text())
//       return null
//     }
//     const responseData = await response.json()
//     if (responseData && Array.isArray(responseData.children)) {
//       // Create a new node object with the children
//       const newNode = {
//         ...node,
//         children: responseData.children
//       }
//       // set an expanded for each child to false
//       newNode.children.forEach((child: any) => {
//         child.expanded = false
//       })
//       // update dep property of the new node based on if "dep" key is present in the response, otherwise set it to null
//       newNode.dep = responseData.dep ? responseData.dep : null
//       return newNode
//     } else {
//       console.error('Invalid response:', responseData)
//       return null
//     }
//   } catch (error: any) {
//     if (error instanceof TypeError) {
//       // Network error or other fetch-related error
//       console.error('Network error:', error.message)
//     } else {
//       // Something else happened
//       console.error('Error:', error.message)
//     }
//     return null
//   }
// }

// async function testfetch() {
//   console.log(data.value)
//   let newdata = await fetchChildren(data.value)
//   if (newdata) {
//     // update the data object with the new node
//     data.value = newdata
//     console.log(data.value)
//   }
// }

// testfetch()

// Reference to the SVG element
const svgRef = ref<SVGSVGElement | null>(null)

// Graph dimensions
const width: number = window.innerWidth
const height: number = window.innerHeight

// Graph layout
const nodeRadius: number = 7
const nodeDistanceX: number = 25
const nodeDistanceY: number = 350
const initialGraphX: number = (width / 7) * 1
const initialGraphY: number = (height / 7) * 3
const zoomScale: [number, number] = [0.25, 5]

// D3 variables
let svg: any
let root: any

const sampleData = {
  id: 'root',
  label: 'Root',
  has_children: true,
  dep: null,
  expanded: false,
  children: [
    {
      id: 'child1',
      label: 'Child 1',
      has_children: true,
      dep: null,
      expanded: false,
      children: [
        {
          id: 'grandchild1',
          label: 'Grandchild 1',
          has_children: false,
          dep: null,
          expanded: false
        },
        {
          id: 'grandchild2',
          label: 'Grandchild 2',
          has_children: false,
          dep: null,
          expanded: false
        }
      ]
    },
    {
      id: 'child2',
      label: 'Child 2',
      has_children: true,
      dep: null,
      expanded: false,
      children: [
        {
          id: 'grandchild3',
          label: 'Grandchild 3',
          has_children: false,
          dep: null,
          expanded: false
        },
        {
          id: 'grandchild4',
          label: 'Grandchild 4',
          has_children: false,
          dep: null,
          expanded: false
        },
        {
          id: 'grandchild5',
          label: 'Grandchild 5',
          has_children: false,
          dep: null,
          expanded: false
        },
        {
          id: 'grandchild6',
          label: 'Grandchild 6',
          has_children: false,
          dep: null,
          expanded: false
        },
        {
          id: 'grandchild7',
          label: 'Grandchild 7',
          has_children: true,
          dep: null,
          expanded: false,
          children: [
            {
              id: 'greatgrandchild1',
              label: 'Great Grandchild 1',
              has_children: false,
              dep: null,
              expanded: false
            },
            {
              id: 'greatgrandchild2',
              label: 'Great Grandchild 2',
              has_children: false,
              dep: null,
              expanded: false
            }
          ]
        }
      ]
    }
  ]
}

// onMounted hook - initialise the graph and render it with just the root node
onMounted(() => {
  initialiseGraph(sampleData)
  // updateGraph(sampleData)
})

// Watcher
watch(
  () => data.value,
  (newData) => {
    if (newData) {
      updateGraph(newData)
    }
  }
)

// initialise the graph area with the SVG element and reposition it to the center vertically
function initialiseGraph(data: any) {
  svg = d3
    .select<SVGSVGElement, unknown>(svgRef.value as SVGSVGElement)
    .attr('width', width)
    .attr('height', height)
    // .style('background-color', '#f00F30')
    .call(d3.zoom<SVGSVGElement, unknown>().on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', d3.zoomIdentity.translate(initialGraphX, initialGraphY).toString())

  // Add an arrow marker for the links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 17)
    .attr('refY', 0)
    .attr('markerWidth', 5)
    .attr('markerHeight', 5)
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#444')

  // Add an arrow marker for extra links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow-extra')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 17)
    .attr('refY', 0)
    .attr('markerWidth', 5)
    .attr('markerHeight', 5)
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'red')

  createGraph(data)
}

// create the graph with the given data
function createGraph(data: any) {
  // Create a new tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])

  // Create a root node from the data
  root = d3.hierarchy(data)

  // Compute the layout
  tree(root)

  // Get the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // render the links
  renderLinks(links)

  // render the nodes
  renderNodes(nodes)

  // render the labels
  renderLabels(nodes)
}

// render the nodes
function renderNodes(nodes: any) {
  const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)

  // Update existing nodes
  nodeSelection.attr('transform', (d: any) => `translate(${d.y},${d.x})`)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', (d: any) => `translate(${d.y},${d.x})`)

  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
    .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
    .attr('stroke', '#444')
    .attr('stroke-width', 2)
    .on('click', (event: Event, d: any) => toggleCollapse(d))

  // Remove old nodes
  nodeSelection.exit().remove()
}

// toggle the collapse of a node
function toggleCollapse(node: any) {
  if (node.children) {
    // if the node is expanded, collapse it
    node._children = node.children
    node.children = null
    node.data.expanded = false
    console.log('Collapsed node:', node.data.label)
  } else if (node._children) {
    // if the node is collapsed, expand it
    node.children = node._children
    node._children = null
    node.data.expanded = true
    console.log('Expanded node:', node.data.label)
  } else {
    // if the node has no children
    console.log('Node has no children:', node.data.label)
    return
  }
  // Trigger the update to re-render the graph with the changes
  updateGraph(node)
}

// update the graph for a specific node's subtree
function updateGraph(node: any) {
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  const nodes = root.descendants()
  const links = root.links()

  // Filter nodes and links to update only the affected subtree
  const subtreeNodes = nodes.filter(
    (d: any) =>
      d.data.id === node.data.id ||
      d.ancestors().some((ancestor: any) => ancestor.data.id === node.data.id)
  )
  const subtreeLinks = links.filter(
    (d: any) =>
      d.source.data.id === node.data.id ||
      d.source.ancestors().some((ancestor: any) => ancestor.data.id === node.data.id)
  )

  renderNodes(subtreeNodes)
  renderLinks(subtreeLinks)
  renderLabels(subtreeNodes)

  console.log('Subtree updated for node:', node.data.label)
}

// render the links
function renderLinks(links: any) {
  const diagonal = d3
    .linkHorizontal()
    .x((d: any) => d.y)
    .y((d: any) => d.x)

  // Select the group for links or create it if it doesn't exist
  let linkGroup = svg.select('g.links')
  if (linkGroup.empty()) {
    linkGroup = svg.append('g').attr('class', 'links')
  }

  const linkSelection = linkGroup.selectAll('path').data(links, (d: any) => d.target.data.id)

  // Update existing links
  linkSelection.attr('d', diagonal)

  // Enter new links
  linkSelection
    .enter()
    .append('path')
    .attr('d', diagonal)
    .attr('fill', 'none')
    .attr('stroke', '#ccc')
    .attr('stroke-width', 2)
    .attr('marker-end', 'url(#arrow)')

  // Remove old links
  linkSelection.exit().remove()
}

// render the labels
function renderLabels(nodes: any) {
  const labelSelection = svg.selectAll('text').data(nodes, (d: any) => d.data.id)

  // Update existing labels
  labelSelection
    .attr('x', (d: any) => d.y)
    .attr('y', (d: any) => d.x)
    .attr('dx', (d: any) => (d.children ? -20 : 10))
    .attr('text-anchor', (d: any) => (d.children ? 'end' : 'start'))
    .text((d: any) => d.data.label)

  // Enter new labels
  labelSelection
    .enter()
    .append('text')
    .attr('x', (d: any) => d.y)
    .attr('y', (d: any) => d.x)
    .attr('dy', '0.35em')
    .attr('dx', (d: any) => (d.children ? -20 : 10))
    .attr('text-anchor', (d: any) => (d.children ? 'end' : 'start'))
    .attr('font-size', '12px')
    .attr('font-family', 'Arial, sans-serif')
    .attr('fill', '#333')
    .text((d: any) => d.data.label)

  // Remove old labels
  labelSelection.exit().remove()
}

// zoom function
function zoomed(event: d3.D3ZoomEvent<SVGSVGElement, any>) {
  const transform = event.transform

  // Combine the new transform with the initial transform
  const combinedTransform = d3.zoomIdentity
    .translate(initialGraphX + transform.x, initialGraphY + transform.y)
    .scale(transform.k)

  svg.attr('transform', combinedTransform.toString())
}
</script>

<script lang="ts">
export default {
  name: 'GraphVisualisation'
}
</script>

<template>
  <svg ref="svgRef"></svg>
</template>

<style scoped></style>
