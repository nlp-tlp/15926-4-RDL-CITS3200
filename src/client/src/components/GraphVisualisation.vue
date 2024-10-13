<script setup lang="ts">
import { useWindowSize } from '@vueuse/core'
import * as d3 from 'd3'
import { onMounted, ref, watch } from 'vue'

import { fetchSelectedInfo } from '../assets/apiFunctions'
import { drawChildrenGraph } from '../assets/childrenGraphFunctions'
import { drawParentsGraph } from '../assets/parentsGraphFunctions'

const props = defineProps({
  /**
   * The flag to include deprecated nodes in the graph.
   */
  includeDeprecated: {
    type: Boolean,
    default: false
  },
  /**
   * The ID of the selected node from the search results for which to fetch the children.
   */
  selectedNodeId: {
    type: String,
    default: 'http://data.15926.org/dm/Thing'
  },
  /**
   * The flag to show labels on the graph nodes.
   */
  showLabels: {
    type: Boolean,
    default: true
  },
  /**
   * The distance between nodes on the X-axis.
   */
  nodeDistanceX: {
    type: Number,
    default: 45
  },
  /**
   * The distance between nodes on the Y-axis.
   */
  nodeDistanceY: {
    type: Number,
    default: 450
  }
})

// Reference to the SVG element
const svgRef = ref<SVGSVGElement | null>(null)

// Get reactive window size from VueUse
const { width, height } = useWindowSize()

// Graph layout
let initialGraphX: number = (width.value / 7) * 2.5 // Center the graph horizontally
let initialGraphY: number = (height.value / 7) * 3
const zoomScale: [number, number] = [0.25, 5]

// D3 variables
let svg: any
let childrenRoot: any
let parentsRoot: any

// Define the emit function to emit the label-clicked event
const emit = defineEmits(['label-clicked'])

/**
 * Watch for changes in window size and update the graph dimensions and transform.
 */
watch([width, height], () => {
  // Update the initial graph layout values
  initialGraphX = (width.value / 7) * 2.5
  initialGraphY = (height.value / 7) * 3

  // Update the SVG dimensions
  d3.select(svgRef.value).attr('width', width.value).attr('height', height.value)

  // Reapply the zoom transform
  svg.attr('transform', d3.zoomIdentity.translate(initialGraphX, initialGraphY).toString())
})

// onMounted hook to initialise the graph and render with the initial data - prop `Thing` as initial node before search
onMounted(() => {
  initialiseGraph()
  fetchSelectedInfo(props.selectedNodeId, props.includeDeprecated).then((data) => {
    drawChildrenGraph(data, childrenRoot, svg, props, emit)
    drawParentsGraph(data, parentsRoot, svg, props, emit)
  })
})

// Watch the selected node ID prop and if it changes, re-render the graph with the new data
watch(
  () => props.selectedNodeId,
  (newVal, oldVal) => {
    fetchSelectedInfo(newVal, props.includeDeprecated).then((data) => {
      drawChildrenGraph(data, childrenRoot, svg, props, emit)
      drawParentsGraph(data, parentsRoot, svg, props, emit)
    })
  }
)

// Watch the includeDeprecated prop and re-render the graph when it changes
watch(
  () => props.includeDeprecated,
  (newVal, oldVal) => {
    fetchSelectedInfo(props.selectedNodeId, props.includeDeprecated).then((data) => {
      drawChildrenGraph(data, childrenRoot, svg, props, emit)
      drawParentsGraph(data, parentsRoot, svg, props, emit)
    })
  }
)

// Watch the showLabels prop and re-render the graph when it changes
watch(
  () => props.showLabels,
  (newVal, oldVal) => {
    fetchSelectedInfo(props.selectedNodeId, props.includeDeprecated).then((data) => {
      drawChildrenGraph(data, childrenRoot, svg, props, emit)
      drawParentsGraph(data, parentsRoot, svg, props, emit)
    })
  }
)

/**
 * Initialises the graph by creating the SVG element and adding the zoom behaviour.
 */
function initialiseGraph() {
  // Create the SVG element
  svg = d3
    .select(svgRef.value as SVGSVGElement)
    .attr('width', width.value)
    .attr('height', height.value)
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

  // Add arrow marker for extra links
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
}

/**
 * Zoom event handler for the graph.
 * Combines the initial transform of centering the graph with the new transform of the zoom event.
 * @param {Object} event - The D3 zoom event object.
 */
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
/**
 * Graph visualisation component to render the children and parents graph of the selected node.
 * The component uses D3.js to render the graph.
 *
 * @param {boolean} includeDeprecated - Flag to include deprecated nodes in the graph.
 * @param {string} selectedNodeId - The ID of the selected node for which to render the graph.
 * @param {boolean} showLabels - Flag to show labels on the graph nodes.
 *
 * @example
 * <GraphVisualisation includeDeprecated selectedNodeId="http://data.15926.org/dm/Thing" showLabels />
 * <GraphVisualisation :includeDeprecated="false" :selectedNodeId="selectedNodeId" :showLabels="true" />
 * <GraphVisualisation />
 */
export default {
  name: 'GraphVisualisation'
}
</script>

<template>
  <svg ref="svgRef"></svg>
</template>

<style scoped></style>
