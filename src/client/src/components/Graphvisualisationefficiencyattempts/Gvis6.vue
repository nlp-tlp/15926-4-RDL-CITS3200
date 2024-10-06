<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, reactive, ref, watch } from 'vue'

import { fetchChildren, getHierarchy } from '../apiFunctions'

// SEPARATE OUT FUNCTIONS, USE DIFF REF DATA FOR GLOBAL AND LOCAL VIEWS, DO I NEED REF IF ONLY UPDATING ON CLICK?
// IM DOUBLE UPDATING CAUSE TOGGLE COLLAPSE UPDATES THE DATA OBJECT AND CALLS UPDATE AND THEN THE WATCHER UPDATES THE GRAPH

// initial data for the root of the global view
const globalRootNode = {
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true
}

// initial data for the node that is selected for the local view
const localSearchedNode = {
  centre_id: 'http://data.15926.org/rdl/RDS2220023',
  has_children: true // include this in returned data from server
}

let globalHierarchyData = reactive(globalRootNode)
let localHierarchyData = reactive(localSearchedNode)

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

// onMounted hook - initialise the graph and render it
onMounted(() => {
  initialiseGraph()
  drawGlobalGraph(globalHierarchyData)
})

// Watch for changes in the data object and re-render the graph

/**
 * Initialise the graph with the SVG element and reposition it to the center vertically.
 */
function initialiseGraph() {
  svg = d3
    .select(svgRef.value as SVGSVGElement)
    .attr('width', width)
    .attr('height', height)
    // .style('background-color', 'red')
    .call(d3.zoom().scaleExtent(zoomScale).on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', d3.zoomIdentity.translate(initialGraphX, initialGraphY).toString())

  // Add the arrow marker for the links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 22)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', '#444')

  // add arrow marker for extra links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow-extra')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 22)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'red')

  // console.log('Initialised graph')
}

/**
 * Zoom function for the graph.
 * Combines the initial transform of centering the graph with the new transform of the zoom event.
 * @param event The zoom event.
 */
function zoomed(event: d3.D3ZoomEvent<SVGSVGElement, any>) {
  const transform = event.transform

  // Combine the new transform with the initial transform
  const combinedTransform = d3.zoomIdentity
    .translate(initialGraphX + transform.x, initialGraphY + transform.y)
    .scale(transform.k)

  svg.attr('transform', combinedTransform.toString())
}

// draw the graph for the global view
function drawGlobalGraph(data: any) {
  // Construct root node from the data
  root = d3.hierarchy(data)

  // Create a tree layout
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  // assign x and y properties to the root and its descendants
  tree(root)

  // Get all the nodes and links
  const nodes = root.descendants()
  const links = root.links()

  // Render the nodes and links
  renderNodes(nodes)
  renderLinks(links)
  renderExtraLinks(nodes)

  // console.log('Global graph drawn')
}

// update
function updateGlobalGraph(data: any) {
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.children : null))

  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  const nodes = root.descendants()
  const links = root.links()

  renderNodes(nodes)
  renderLinks(links)
  renderExtraLinks(nodes)

  // console.log('Global graph updated')
}

// render the nodes of the graph - uses nodes array
function renderNodes(nodes: any) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)
  // console.log('Nodes:', nodes)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => toggleCollapse(d))

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    // set the fill color based on the presence of children
    .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
    // set the cursor style based on the presence of children
    .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
    .attr('stroke', '#444')
    .attr('stroke-width', 2)

  // append text to the node
  nodeEnter
    .append('text')
    .attr('dy', '.35em')
    // set the text position based on the expanded state - left if expanded, right if collapsed
    .attr('x', (d: any) => (d.data.expanded ? -10 : 10))
    .style('text-anchor', (d: any) => (d.data.expanded ? 'end' : 'start'))
    .text((d: any) => d.data.label)

  // merge the enter and update selections
  const nodeUpdate = nodeEnter.merge(nodeSelection)

  // Update the node positions and visibility
  nodeUpdate
    .attr('transform', (d: any) => `translate(${d.y},${d.x})`)
    .style('display', (d: any) => (d.parent && !d.parent.data.expanded ? 'none' : null))

  // Update the text position based on the expanded state
  nodeUpdate
    .select('text')
    .attr('x', (d: any) => (d.data.expanded ? -10 : 10))
    .style('text-anchor', (d: any) => (d.data.expanded ? 'end' : 'start'))

  // remove the nodes that are no longer needed
  nodeSelection.exit().remove()

  // console.log('Rendered nodes')
}

// toggle the collapse/expansion of a node
async function toggleCollapse(node: any) {
  if (!node.data.has_children) {
    console.log('Node has no children:', node.data.label)
    return
  }

  if (!node.data.children) {
    // Fetch the children of the node
    let newNodeData = await fetchChildren(node.data)
    updateGlobalHierarchyData(node.data.id, newNodeData)
  } else {
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }

  updateGlobalGraph(globalHierarchyData)
}

// find the node in globalHierarchyData and update it
function updateGlobalHierarchyData(nodeId: string, newNodeData: any) {
  function updateNode(node: any): boolean {
    if (node.id === nodeId) {
      node.children = newNodeData.children.map((child: any) => ({
        ...child,
        expanded: false,
        children: null
      }))
      node.expanded = true
      return true
    }

    if (node.children) {
      for (let child of node.children) {
        if (updateNode(child)) {
          return true
        }
      }
    }

    return false
  }

  updateNode(globalHierarchyData)
}

// render the links of the graph
function renderLinks(links: any) {
  // Select all links and bind the data
  const link = svg.selectAll('path.link').data(links, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const linkEnter = link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link')
    .attr('stroke', '#999')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')

  // merge the enter and update selections
  const linkUpdate = linkEnter.merge(link)

  // update the link positions
  linkUpdate.attr('d', diagonal)

  // remove the links that are no longer needed
  link.exit().remove()

  // console.log('Rendered links')
}

// render the extra links of the graph
function renderExtraLinks(nodes: any) {
  // Create an array to store the extra links
  const extraLinks: any = []
  // Iterate over the nodes to find the extra links
  nodes.forEach((d: any) => {
    if (d.data.extra_parents) {
      d.data.extra_parents.forEach((parent: any) => {
        const parentNode = nodes.find((node: any) => node.data.id === parent.id)
        if (parentNode) {
          extraLinks.push({ source: parentNode, target: d })
        }
      })
    }
  })

  // Select all extra links and bind the data
  const extraLink: any = svg.selectAll('path.extra-link').data(extraLinks, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const extraLinkEnter = extraLink
    .enter()
    .insert('path', 'g')
    .attr('class', 'extra-link')
    .attr('stroke', 'red')
    .attr('stroke-width', 1)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow-extra)')
    .attr('stroke-dasharray', '5,5')

  // merge the enter and update selections
  const extraLinkUpdate = extraLinkEnter.merge(extraLink)

  // update the extra link positions to use the diagonal function
  extraLinkUpdate.attr('d', diagonal)

  // remove the extra links that are no longer needed
  extraLink.exit().remove()

  // console.log('Rendered extra links')
}

// /**
//  * Render the graph with the data object from the props.
//  */
// function renderGraph() {
//   // Check if the data object is available
//   if (!data.value) {
//     return
//   }

//   // Create a hierarchy from the data object
//   root = d3.hierarchy(data.value)
//   // update the graph based on the new data in the props
//   update(root)
// }

// async function renderLocalGraph() {
//   // Check if the data object is available
//   if (!data.value) {
//     return
//   }

//   const node = await getHierarchy(data.value)
//   console.log('Node:', node)
//   if (node) {
//     // Create a hierarchy from the data object
//     root = d3.hierarchy(node.hierarchy)
//     console.log('Root:', root)
//     // update the graph based on the new data in the props
//     update(root)
//   }

//   // Create a hierarchy from the data object
//   // root = d3.hierarchy(data)
//   // update the graph based on the new data in the props
//   // update(root)
// }

// /**
//  * Update the graph with the new data.
//  * @param source The source node.
//  */
// function update(source: any) {
//   // Create a tree layout with the node distance
//   const treeLayout = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
//   const treeData = treeLayout(root as unknown as d3.HierarchyNode<unknown>)

//   // Get the nodes and links
//   const nodes = treeData.descendants()
//   const links = treeData.links()

//   // Render the nodes, links, and extra links
//   renderNodes(nodes)
//   renderLinks(links)
//   renderExtraLinks(nodes)

//   // re collapse the nodes that were previously collapsed for consistency
//   hidePreviousCollapsedNodes(nodes)
// }

// /**
//  * Hide the nodes that were previously collapsed.
//  * @param nodes The nodes to be checked.
//  */
// function hidePreviousCollapsedNodes(nodes: any) {
//   nodes.forEach((d: any) => {
//     // Check if the node was previously collapsed but the children are currently visible
//     if (d.data.expanded === false && d.children) {
//       d._children = d.children
//       d.children = null
//     }
//   })
// }

// /**
//  * Toggle the collapse of a node.
//  * @param node The node to be toggled.
//  */
// async function toggleCollapse(node: any) {
//   // Check if the node has children
//   if (node.data.has_children) {
//     // Check if the children have not been fetched
//     if (!node.children && !node._children) {
//       // Fetch the children of the node
//       await fetchChildren(node.data)

//       // Expand the node
//       node.children = node._children
//       node._children = null
//       node.data.expanded = true
//       console.log('Expanded node:', node.data.label)
//     } else {
//       // if the children are hidden
//       if (node._children) {
//         // Expand the node
//         node.children = node._children
//         node._children = null
//         node.data.expanded = true
//         console.log('Expanded node:', node.data.label)
//       }
//       // if the children are visible
//       else if (node.children) {
//         // Collapse the node
//         node._children = node.children
//         node.children = null
//         node.data.expanded = false
//         console.log('Collapsed node:', node.data.label)
//       }
//     }
//   } else {
//     // if the node has no children
//     console.log('Node has no children:', node.data.label)
//     return
//   }
//   // Trigger the update to re-render the graph with the changes
//   update(node)
// }

// /**
//  * Render the nodes of the graph.
//  * @param nodes The nodes to be rendered.
//  */
// function renderNodes(nodes: any) {
//   // Select all nodes and bind the data
//   const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)

//   // on enter, append the node group and add the circle and text elements
//   const nodeEnter: any = nodeSelection
//     .enter()
//     .append('g')
//     .attr('class', 'node')
//     // on click, toggle the collapse of the node
//     .on('click', (event: Event, d: any) => toggleCollapse(d))

//   nodeEnter
//     .append('circle')
//     .attr('r', nodeRadius)
//     // set the fill color based on the presence of children
//     .attr('fill', (d: any) => (d.data.has_children ? '#69b3a2' : '#999'))
//     // set the cursor style based on the presence of children
//     .attr('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
//     .attr('stroke', '#444')
//     .attr('stroke-width', 2)

//   nodeEnter
//     .append('text')
//     .attr('dy', '.35em')
//     // set the text position based on the expanded state - left if expanded, right if collapsed
//     .attr('x', (d: any) => (d.data.expanded ? -10 : 10))
//     .style('text-anchor', (d: any) => (d.data.expanded ? 'end' : 'start'))
//     .text((d: any) => d.data.label)

//   // merge the enter and update selections
//   const nodeUpdate = nodeEnter.merge(nodeSelection)

//   // update the node positions
//   nodeUpdate.attr('transform', (d: any) => `translate(${d.y},${d.x})`)

//   // remove the nodes that are no longer needed
//   nodeSelection.exit().remove()
// }

// /**
//  * Render the links of the graph.
//  * @param links The links to be rendered.
//  */
// function renderLinks(links: any, colour: string = '#999') {
//   // Select all links and bind the data
//   const link: any = svg.selectAll('path.link').data(links, (d: any) => d.target.id)

//   // on enter, insert the path element and set the attributes
//   const linkEnter = link
//     .enter()
//     .insert('path', 'g')
//     .attr('class', 'link')
//     .attr('stroke', colour)
//     .attr('fill', 'none')
//     .attr('marker-end', 'url(#arrow)')

//   // merge the enter and update selections
//   const linkUpdate = linkEnter.merge(link)

//   linkUpdate.attr('d', diagonal)

//   link.exit().remove()
// }

// /**
//  * Render the extra links of the graph.
//  * @param nodes The nodes to be used for the extra links.
//  */
// function renderExtraLinks(nodes: any, colour: string = 'red') {
//   // Create an array to store the extra links
//   const extraLinks: any = []
//   // Iterate over the nodes to find the extra links
//   nodes.forEach((d: any) => {
//     if (d.data.extra_parents) {
//       d.data.extra_parents.forEach((parent: any) => {
//         const parentNode = nodes.find((node: any) => node.data.id === parent.id)
//         if (parentNode) {
//           extraLinks.push({ source: parentNode, target: d })
//         }
//       })
//     }
//   })

//   // Select all extra links and bind the data
//   const extraLink: any = svg.selectAll('path.extra-link').data(extraLinks, (d: any) => d.target.id)

//   // on enter, insert the path element and set the attributes
//   const extraLinkEnter = extraLink
//     .enter()
//     .insert('path', 'g')
//     .attr('class', 'extra-link')
//     .attr('stroke', colour)
//     .attr('fill', 'none')
//     .attr('marker-end', 'url(#arrow-extra)')
//     .attr('stroke-dasharray', '5,5')

//   // merge the enter and update selections
//   const extraLinkUpdate = extraLinkEnter.merge(extraLink)

//   // update the extra link positions to use the diagonal function
//   extraLinkUpdate.attr('d', diagonal)

//   extraLink.exit().remove()
// }

/**
 * Create a diagonal path generator.
 */
const diagonal: any = d3
  .linkHorizontal()
  .x((d: any) => d.y)
  .y((d: any) => d.x)
</script>

<script lang="ts">
/**
 * GraphVisualisation component represents the global graph hierarchy visualisation.
 * It uses D3.js to render the graph with the provided data object.
 * The graph is interactive and allows for collapsing and expanding nodes.
 * The component also fetches the children of a node from the server upon node expansion.
 *
 * @param {Object} data - The reactive data object to be visualised.
 * @param {Function} fetchChildren - Function to fetch the children of a node from the server.
 *
 * @example
 * <GraphVisualisation :data="data" :fetch-children="fetchChildren" />
 */
export default {
  name: 'GraphVisualisation'
}
</script>

<template>
  <svg ref="svgRef"></svg>
</template>

<style scoped></style>
