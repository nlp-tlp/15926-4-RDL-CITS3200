<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, ref, watch } from 'vue'

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
let diagonal: any
let duration: number = 750

// onMounted hook - initialise the graph and render it with just the root node
onMounted(() => {
  initialiseGraph(data.value)
})

// Watcher
watch(
  () => data.value,
  (newData) => {
    if (newData) {
      updateGraph(newData)
      // console.log('Data updated:', newData)
    }
  }
)

// initialise the graph area with the SVG element and reposition it to the center vertically
function initialiseGraph(data: any) {
  svg = d3
    .select<SVGSVGElement, unknown>(svgRef.value as SVGSVGElement)
    .attr('width', width)
    .attr('height', height)
    .call(d3.zoom<SVGSVGElement, unknown>().on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', d3.zoomIdentity.translate(initialGraphX, initialGraphY).toString())

  // // Add an arrow marker for the links
  // svg
  //   .append('defs')
  //   .append('marker')
  //   .attr('id', 'arrow')
  //   .attr('viewBox', '0 -5 10 10')
  //   .attr('refX', 17)
  //   .attr('refY', 0)
  //   .attr('markerWidth', 5)
  //   .attr('markerHeight', 5)
  //   .attr('orient', 'auto')
  //   .attr('markerUnits', 'strokeWidth')
  //   .append('path')
  //   .attr('d', 'M0,-5L10,0L0,5')
  //   .attr('fill', '#444')

  // // Add an arrow marker for extra links
  // svg
  //   .append('defs')
  //   .append('marker')
  //   .attr('id', 'arrow-extra')
  //   .attr('viewBox', '0 -5 10 10')
  //   .attr('refX', 17)
  //   .attr('refY', 0)
  //   .attr('markerWidth', 5)
  //   .attr('markerHeight', 5)
  //   .attr('orient', 'auto')
  //   .attr('markerUnits', 'strokeWidth')
  //   .append('path')
  //   .attr('d', 'M0,-5L10,0L0,5')
  //   .attr('fill', 'red')

  createGraph(data)
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

// create the graph with the given data
function createGraph(data: any) {
  // Create a new tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])

  diagonal = d3
    .linkHorizontal()
    .x((d: any) => d.y)
    .y((d: any) => d.x)

  root = d3.hierarchy(data)

  tree(root)

  root.x0 = initialGraphX
  root.y0 = initialGraphY
  // console.log('Root:', root)
  // console.log('Data:', data)

  // Collapse all children of the root's children before rendering
  // function collapseChildren(d: any) {
  //   if (d.children) {
  //     d._children = d.children
  //     d._children.forEach(collapseChildren)
  //     d.children = null
  //   }
  // }
  // collapseChildren(root)

  // update the graph
  updateGraph(root)
}

// UOPDATE TO USE SOURCE???????

// update the graph for a specific node's subtree
function updateGraph(source: any) {
  console.log('Source:', source)
  console.log('Data:', data.value)
  console.log('Root:', root)

  const nodes = source.descendants()
  console.log('Nodes:', nodes)
  const links = source.links()
  // console.log('Links:', links)

  // Normalize for fixed-depth
  nodes.forEach((d: any) => {
    d.y = d.depth * 180
    d.x = d.x ? d.x : 0
  })

  // Update the nodes
  const node = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)

  // Enter any new nodes at the parent's previous position
  const nodeEnter = node
    .enter()
    .append('g')
    .attr('class', 'node')
    // .attr('transform', (d: any) => `translate(${source.y0},${source.x0})`)
    .on('click', (event: Event, d: any) => toggleCollapse(d))

  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
    .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
    .attr('stroke', '#444')
    .attr('stroke-width', 2)

  nodeEnter
    .append('text')
    .attr('x', (d: any) => (d.children || d._children ? -10 : 10))
    .attr('dy', '.35em')
    .attr('text-anchor', (d: any) => (d.children || d._children ? 'end' : 'start'))
    .text((d: any) => d.data.label)
    .style('fill-opacity', 1e-6)

  // Transition nodes to their new position
  const nodeUpdate = node
    .merge(nodeEnter)
    .transition()
    .duration(duration)
    .attr('transform', (d: any) => `translate(${d.y},${d.x})`)

  nodeUpdate
    .select('circle')
    .attr('r', nodeRadius)
    .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))

  nodeUpdate.select('text').style('fill-opacity', 1)

  // Transition exiting nodes to the parent's new position
  const nodeExit = node
    .exit()
    .transition()
    .duration(duration)
    .attr('transform', (d: any) => `translate(${source.y},${source.x})`)
    .remove()

  nodeExit.select('circle').attr('r', 1e-6)

  nodeExit.select('text').style('fill-opacity', 1e-6)

  // Update the links
  const link = svg.selectAll('path.link').data(links, (d: any) => d.target.data.id)

  // Enter any new links at the parent's previous position
  link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link')
    .attr('d', (d: any) => {
      const o = { x: source.x0 ? source.x0 : 0, y: source.y0 ? source.y0 : 0 }
      return diagonal({ source: o, target: o })
    })
    .attr('fill', 'none')
    .attr('stroke', '#f00')
    .attr('stroke-width', 2)
    .attr('marker-end', 'url(#arrow)')

  // Transition links to their new position
  link.transition().duration(duration).attr('d', diagonal)

  // Transition exiting nodes to the parent's new position
  link
    .exit()
    .transition()
    .duration(duration)
    .attr('d', (d: any) => {
      const o = { x: source.x ? source.x : 0, y: source.y ? source.y : 0 }
      return diagonal({ source: o, target: o })
    })
    .remove()

  // Stash the old positions for transition
  nodes.forEach((d: any) => {
    d.x0 = d.x
    d.y0 = d.y
  })
}

// toggle the collapse of a node
function toggleCollapse(node: any) {
  if (!node.data.has_children) {
    console.log('Node has no children:', node.data.label)
    return
  }
  if (!node.children && !node._children) {
    console.log('Fetching children for node:', node.data.label)
    fetchChildren(node).then((newNode) => {
      if (newNode) {
        // update the data object with the new node
        data.value = newNode
        console.log('Fetched children for node:', node.data.label)
        node.children = d3.hierarchy(newNode).children
      }
    })
  }

  if (node._children) {
    node.children = node._children
    node._children = null
  } else {
    node._children = node.children
    node.children = null
  }

  updateGraph(node)
}

// mock fetchchildren
async function fetchChildren(node: any) {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        id: 'http://data.15926.org/dm/Thing',
        expanded: false,
        children: [
          {
            id: 'http://data.15926.org/dm/Child1',
            label: 'Child 1',
            has_children: true,
            dep: null,
            expanded: false
          },
          {
            id: 'http://data.15926.org/dm/Child2',
            label: 'Child 2',
            has_children: false,
            dep: null,
            expanded: false
          }
        ]
      })
    }, 20)
  })
}

// // render the nodes
// function renderNodes(nodes: any) {
//   const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)

//   // Update existing nodes
//   nodeSelection
//     .attr('transform', (d: any) => `translate(${d.y},${d.x})`)

//   // Enter new nodes
//   const nodeEnter = nodeSelection
//     .enter()
//     .append('g')
//     .attr('class', 'node')
//     .attr('transform', (d: any) => `translate(${d.y},${d.x})`)

//   nodeEnter
//     .append('circle')
//     .attr('r', nodeRadius)
//     .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
//     .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
//     .attr('stroke', '#444')
//     .attr('stroke-width', 2)
//     .on('click', (event: Event, d: any) => toggleCollapse(d))

//   // Remove old nodes
//   nodeSelection.exit().remove()
// }

// // toggle the collapse of a node
// async function toggleCollapse(node: any) {
//   if (node.data.has_children) {
//     if (!node.children && !node._children) {
//       console.log('data before:', data.value)
//       console.log('Fetching children for node:', node.data.label)
//       // fetch the children of the node
//       await fetchChildren(node).then((newNode) => {
//         if (newNode) {
//           // update the data object with the new node
//           data.value = newNode
//           console.log('Fetched children for node:', node.data.label)
//           console.log('New data:', data.value)
//         }
//       })
//       node.children = node._children
//       node._children = null
//       node.data.expanded = true
//       console.log('Expanded node:', node.data.label)
//     } else {
//       if (node._children) {
//         node.children = node._children
//         node._children = null
//         node.data.expanded = true
//         console.log('Expanded node:', node.data.label)
//       } else if (node.children) {
//         node._children = node.children
//         node.children = null
//         node.data.expanded = false
//         console.log('Collapsed node:', node.data.label)
//       }
//     }
//   } else {
//     console.log('Node has no children:', node.data.label)
//     return
//   }
//   updateGraph(node)
// }

// // update the graph for a specific node's subtree
// function updateGraph(node: any) {
//   const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
//   tree(root)

//   const nodes = root.descendants()
//   const links = root.links()

//   // Filter nodes and links to update only the affected subtree
//   const subtreeNodes = nodes.filter((d: any) => d.data.id === node.data.id || d.ancestors().some((ancestor: any) => ancestor.data.id === node.data.id))
//   const subtreeLinks = links.filter((d: any) => d.source.data.id === node.data.id || d.source.ancestors().some((ancestor: any) => ancestor.data.id === node.data.id))

//   renderNodes(subtreeNodes)
//   renderLinks(subtreeLinks)
//   renderLabels(subtreeNodes)

//   console.log('Subtree updated for node:', node.data.label)
// }

// // render the links
// function renderLinks(links: any) {
//   const diagonal = d3
//     .linkHorizontal()
//     .x((d: any) => d.y)
//     .y((d: any) => d.x)

//   // Select the group for links or create it if it doesn't exist
//   let linkGroup = svg.select('g.links')
//   if (linkGroup.empty()) {
//     linkGroup = svg.append('g').attr('class', 'links')
//   }

//   const linkSelection = linkGroup.selectAll('path').data(links, (d: any) => d.target.data.id)

//   // Update existing links
//   linkSelection.attr('d', diagonal)

//   // Enter new links
//   linkSelection
//     .enter()
//     .append('path')
//     .attr('d', diagonal)
//     .attr('fill', 'none')
//     .attr('stroke', '#ccc')
//     .attr('stroke-width', 2)
//     .attr('marker-end', 'url(#arrow)')

//   // Remove old links
//   linkSelection.exit().remove()
// }

// // render the labels
// function renderLabels(nodes: any) {
//   const labelSelection = svg.selectAll('text').data(nodes, (d: any) => d.data.id)

//   // Update existing labels
//   labelSelection
//     .attr('x', (d: any) => d.y)
//     .attr('y', (d: any) => d.x)
//     .attr('dx', (d: any) => (d.children ? -20 : 10))
//     .attr('text-anchor', (d: any) => (d.children ? 'end' : 'start'))
//     .text((d: any) => d.data.label)

//   // Enter new labels
//   labelSelection
//     .enter()
//     .append('text')
//     .attr('x', (d: any) => d.y)
//     .attr('y', (d: any) => d.x)
//     .attr('dy', '0.35em')
//     .attr('dx', (d: any) => (d.children ? -20 : 10))
//     .attr('text-anchor', (d: any) => (d.children ? 'end' : 'start'))
//     .attr('font-size', '12px')
//     .attr('font-family', 'Arial, sans-serif')
//     .attr('fill', '#333')
//     .text((d: any) => d.data.label)

//   // Remove old labels
//   labelSelection.exit().remove()
// }
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
