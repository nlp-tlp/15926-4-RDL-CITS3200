<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, reactive, ref, watch } from 'vue'

import { fetchChildren, getHierarchy } from './apiFunctions'

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
  id: 'http://data.15926.org/rdl/RDS2220023',
  label: 'WROUGHT',
  has_children: true
}

let hierarchyData = reactive(globalRootNode)
// let hierarchyData = reactive(localSearchedNode)

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
  drawForwardGraph(hierarchyData)
  // drawBothSidedGraph(hierarchyData)
})

function drawBothSidedGraph(data: any) {
  // get the hierarchy back from the server to get the path from thing to the node
  getHierarchy(data).then((hierarchy) => {
    // console.log('Hierarchy:', hierarchy)
    // Construct root node from the data
    root = d3.hierarchy(hierarchy.hierarchy)

    // set the hierarchyData to the hierarchy object
    hierarchyData = root.data

    // // Create a tree layout
    const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
    // assign x and y properties to the root and its descendants
    tree(root)

    // set expanded to true for each node in the path from Thing to the node
    root.each((d: any) => {
      d.data.expanded = true
    })

    // Get the nodes and links from Thing to the node - that node has property 'centre: true'
    const nodes = root.descendants()
    const links = root.links()

    // for each node that is not the centre node, set their has_children property to true, for centre dont change it
    nodes.forEach((node: any) => {
      if (!node.data.centre) {
        node.data.has_children = true
      }
    })

    // console.log('Nodes:', nodes)
    // console.log('Links:', links)

    // Render the nodes and links
    renderNodesUpToSearchedNode(nodes, hierarchyData)
    // renderNodes(nodes, hierarchyData)
    // renderLinks(links)
    // renderExtraLinks(nodes)
  })
}

// Render Nodes from Thing to the node\
function renderNodesUpToSearchedNode(nodes: any, data: any) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)
  // console.log('Nodessss:', nodes)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      event.stopPropagation()
      // toggleCollapse(d, data)
      toggleCollapseUpToSearchedNode(d, data)
    })

  // append circle to the node
  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    // set the fill color based on the presence of children
    .attr('fill', (d: any) => {
      if (d.data.centre) {
        return 'red'
      } else if (d.data.has_children) {
        return '#69b3a2'
      } else {
        return '#999'
      }
    })
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

  // // Update the node positions and visibility
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
}

// toggle the children from the searched node onwards but still render the path from Thing to the searched node
async function toggleCollapseUpToSearchedNode(node: any, data: any) {
  if (!node.data.has_children) {
    console.log('Node has no children:', node.data.label)
    return
  }
  // if the node is not the centre node
  // if (!node.data.centre) {
  //   return
  // }

  if (!node.data.children) {
    // Fetch the children of the node
    let newNodeData = await fetchChildren(node.data)
    updateHierarchyDataUpToSearchedNode(node, newNodeData)
    // console.log('New node data:', newNodeData)
    // console.log('hierarchyData:', hierarchyData)
    // console.log('data:', data)
  } else {
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }
  console.log(node.data.expanded ? 'Expanded node:' : 'Collapsed node:', node.data.label)

  // updateForwardGraph(data)
  updateForwardGraphUpToSearchedNode(data)
}

// update the graph from the searched node onwards, so render the path from Thing to the searched node and then the children of the searched node
function updateForwardGraphUpToSearchedNode(data: any) {
  console.log('Data:', data)

  // Create a hierarchy from the data
  const root = d3.hierarchy(data, (d: any) => d.children)

  // Create a tree layout with specified node size
  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  console.log('Root:', root)

  // Get all nodes and links from the hierarchy
  const nodes = root.descendants()
  const links = root.links()

  console.log('Nodes:', nodes)
  console.log('Links:', links)

  // Render nodes and links
  renderNodesUpToSearchedNode(nodes, hierarchyData)
  // renderLinks(links);
}

// the returned data from the server is the hierarchy from Thing to the node, so update the hierarchyData object and the searched node
function updateHierarchyDataUpToSearchedNode(node: any, newNodeData: any) {
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      currentNode.children = newNodeData.children.map((child: any) => ({
        ...child,
        expanded: true,
        children: null
      }))
      currentNode.expanded = true
      return true
    }

    if (currentNode.children) {
      for (let child of currentNode.children) {
        if (updateNode(child)) {
          return true
        }
      }
    }

    return false
  }

  updateNode(hierarchyData)
}

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

// draw the graph - can be forward expanded
function drawForwardGraph(data: any) {
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
  renderNodes(nodes, hierarchyData)
  renderLinks(links)
  renderExtraLinks(nodes)
}

// update
function updateForwardGraph(data: any) {
  root = d3.hierarchy(data, (d: any) => (d.expanded ? d.children : null))

  const tree = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  tree(root)

  const nodes = root.descendants()
  const links = root.links()

  renderNodes(nodes, hierarchyData)
  renderLinks(links)
  renderExtraLinks(nodes)
}

// render the nodes of the graph - uses nodes array
function renderNodes(nodes: any, data: any) {
  // Select all nodes and bind the data
  const nodeSelection = svg.selectAll('g.node').data(nodes, (d: any) => d.data.id)
  // console.log('Nodes:', nodes)

  // Enter new nodes
  const nodeEnter = nodeSelection
    .enter()
    .append('g')
    .attr('class', 'node')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => {
      event.stopPropagation()
      toggleCollapse(d, data)
    })

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
}

// toggle the collapse/expansion of a node
async function toggleCollapse(node: any, data: any) {
  if (!node.data.has_children) {
    console.log('Node has no children:', node.data.label)
    return
  }

  if (!node.data.children) {
    // Fetch the children of the node
    let newNodeData = await fetchChildren(node.data)
    updateHierarchyData(node, newNodeData)
  } else {
    // Toggle the expanded state
    node.data.expanded = !node.data.expanded
  }
  console.log(node.data.expanded ? 'Expanded node:' : 'Collapsed node:', node.data.label)

  updateForwardGraph(data)
}

// find the node in hierarchyData and update it
function updateHierarchyData(node: any, newNodeData: any) {
  function updateNode(currentNode: any): boolean {
    if (currentNode === node.data) {
      currentNode.children = newNodeData.children.map((child: any) => ({
        ...child,
        expanded: false,
        children: null
      }))
      currentNode.expanded = true
      return true
    }

    if (currentNode.children) {
      for (let child of currentNode.children) {
        if (updateNode(child)) {
          return true
        }
      }
    }

    return false
  }

  updateNode(hierarchyData)
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
}

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
