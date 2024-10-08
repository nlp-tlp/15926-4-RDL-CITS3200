<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, reactive, ref, watch } from 'vue'

import { fetchSelectedInfo } from '../assets/apiFunctions';
import { drawChildrenGraph } from '../assets/childrenGraphFunctions'
import { drawParentsGraph } from '../assets/parentsGraphFunctions';


const props = defineProps({
  includeDeprecated: Boolean,
  selectedNodeId: String
})


watch(() => props.selectedNodeId, (newVal, oldVal) => {
  fetchSelectedInfo(newVal).then((data) => {
    drawChildrenGraph(data, childrenRoot, svg, props.includeDeprecated)
    drawParentsGraph(data, parentsRoot, svg, props.includeDeprecated)

  })
})


// initial data for the root of the global view
const selectedNodeDataChildren = {
  // id: 'http://data.15926.org/rdl/RDS458774',
  // label: 'SEAMLESS ARTEFACT',
  // has_children: true,
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_children: true,
}
const selectedNodeDataParents = {
  // id: 'http://data.15926.org/rdl/RDS458774',
  // label: 'SEAMLESS ARTEFACT',
  // has_parents: true,
  id: 'http://data.15926.org/dm/Thing',
  label: 'Thing',
  has_parents : false,
}


let childrenHierarchyData = reactive(selectedNodeDataChildren)
let parentHierarchyData = reactive(selectedNodeDataParents)

// Reference to the SVG element
const svgRef = ref<SVGSVGElement | null>(null)

// Graph dimensions
const width: number = window.innerWidth
const height: number = window.innerHeight

// Graph layout

const initialGraphX: number = (width / 7) * 3.5
const initialGraphY: number = (height / 7) * 3
const zoomScale: [number, number] = [0.25, 5]

// D3 variables
let svg: any
let childrenRoot: any
let parentsRoot: any

// onMounted hook - initialise the graph and render it
onMounted(() => {
  initialiseGraph()
  drawChildrenGraph(childrenHierarchyData, childrenRoot, svg, props.includeDeprecated)
  drawParentsGraph(parentHierarchyData, parentsRoot, svg, props.includeDeprecated)
  
})

// watch(() => props.includeDeprecated, (newVal, oldVal) => {
//   console.log('includeDeprecated', newVal)
//   initialiseGraph()
//   drawChildrenGraph(childrenHierarchyData, root, svg, newVal)
// })



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
    .attr('refX', 0)
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
    .attr('refX', 0)
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


//  draw the parents graph















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