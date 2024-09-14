<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  /**
   * The JSON data to visualise as a graph.
   *
   * @type {Object}
   * @required
   * @example
   *  {
   *    label: 'root',
   *    children: [
   *      {
   *        label: 'child1',
   *        children: [],
   *        extra_parents: []
   *      },
   *      {
   *        label: 'child2',
   *        children: []
   *      }
   *    ]
   *  }
   */
  data: {
    type: Object,
    required: true
  }
})

const svgRef = ref<Element>()

// width and height to fit the whole parent container
// Need to figure out how to dynamically adjust based on other elements e.g. sidepane and navbar as this is why scrollbars are appearing
const width = window.innerWidth
const height = window.innerHeight
const nodeDistance = 20
const initialGraphX = (width / 7) * 1
const initialGraphY = (height / 7) * 3

let svg: any
let root: any

onMounted(() => {
  initialiseGraph()
  renderGraph()
})

// watcher for data changes
watch(
  () => props.data,
  (newData) => {
    if (newData) {
      renderGraph()
    }
  }
)

/**
 * Initialises the graph by creating the SVG element and setting up the zoom behaviour.
 */
function initialiseGraph() {
  svg = d3
    .select(svgRef.value as Element)
    .attr('width', width)
    .attr('height', height)
    .call(d3.zoom().scaleExtent([0.5, 5]).on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', `translate(${initialGraphX},${initialGraphY})`)

  const initialTransform = d3.zoomIdentity.translate(initialGraphX, initialGraphY)

  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 16)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto-start-reverse')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'black')

  d3.select(svgRef.value as Element).call(d3.zoom().transform as any, initialTransform)
}

/**
 * Zooms the graph.
 *
 * @param {Object} event - The zoom event.
 */
function zoomed(event: any) {
  svg.attr('transform', event.transform)
}

/**
 * Renders the graph.
 */
function renderGraph() {
  if (!props.data) {
    return
  }

  const startTime = performance.now()

  root = d3.hierarchy(props.data)

  update(root)

  const endTime = performance.now()
  console.log(`Rendering took ${endTime - startTime} ms`)
}

/**
 * Updates the graph with the given source node.
 *
 * @param {Object} source - The source node.
 */
function update(source: any) {
  const treeLayout = d3.tree().nodeSize([nodeDistance, 300])
  const treeData = treeLayout(root as unknown as d3.HierarchyNode<unknown>)

  const nodes = treeData.descendants()
  const links = treeData.links()

  nodes.forEach((d) => (d.y = d.depth * 180))

  renderNodes(nodes)
  renderLinks(links, source)
  renderExtraLinks(nodes)
}

/**
 * Renders the nodes.
 *
 * @param {Object[]} nodes - The nodes to render.
 */
function renderNodes(nodes: any) {
  const node = svg.selectAll('g.node').data(nodes, (d: any) => d.id || (d.id = d.data.id))

  const nodeEnter: any = node
    .enter()
    .append('g')
    .attr('class', 'node')
    .on('click', (event: Event, d: any) => toggleCollapse(d))
    .style('cursor', (d: any) => (d.children || d._children ? 'pointer' : 'default'))

  nodeEnter
    .append('circle')
    .attr('r', 5)
    .style('fill', (d: any) => (d._children ? 'lightsteelblue' : '#999'))

  nodeEnter
    .append('text')
    .attr('dy', '.35em')
    .attr('x', (d: any) => (d.children || d._children ? -10 : 10))
    .style('text-anchor', (d: any) => (d.children || d._children ? 'end' : 'start'))
    .text((d: any) => d.data.label)

  const nodeUpdate = nodeEnter.merge(node)

  nodeUpdate.attr('transform', (d: any) => `translate(${d.y},${d.x})`)

  nodeUpdate
    .select('circle')
    .attr('r', 5)
    .style('fill', (d: any) => (d._children ? 'lightsteelblue' : '#999'))

  node.exit().remove()
}

/**
 * Renders the links.
 *
 * @param {Object[]} links - The links to render.
 * @param {Object} source - The source node.
 */
function renderLinks(links: any, source: any) {
  const link: any = svg.selectAll('path.link').data(links, (d: any) => d.target.id)

  const linkEnter = link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link')
    .attr('stroke', 'black')
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')

  const linkUpdate = linkEnter.merge(link)

  linkUpdate.attr('d', diagonal)

  link.exit().remove()
}

/**
 * Renders the extra links.
 *
 * @param {Object[]} nodes - The nodes to render the extra links for.
 */
function renderExtraLinks(nodes: any) {
  const extraLinks: any = []
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

  const extraLink = svg.selectAll('path.extra-link').data(extraLinks)

  extraLink
    .enter()
    .insert('path', 'g')
    .attr('class', 'extra-link')
    .attr('stroke', 'red')
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')
    .attr('d', (d: any) => diagonal({ source: d.source, target: d.target }))

  extraLink.merge(extraLink).attr('d', (d: any) => diagonal({ source: d.source, target: d.target }))

  extraLink.exit().remove()
}

/**
 * Toggles the collapse of the given node.
 *
 * @param {Object} d - The node to toggle the collapse for.
 */
function toggleCollapse(d: any) {
  if (d.children) {
    d._children = d.children
    d.children = null
  } else {
    d.children = d._children
    d._children = null
  }
  update(d)
}

const diagonal: any = d3
  .linkHorizontal()
  .x((d: any) => d.y)
  .y((d: any) => d.x)
</script>

<script lang="ts">
/**
 * GraphVisualisation component represents the visualisation of a graph.
 *
 * This component uses D3.js to render the graph.
 *
 * @param {Object} data - The JSON data to visualise as a graph.
 *
 * Contains the following properties:
 * @param {string} data.label - The label of the node.
 * @param {Object[]} [data.children] - The child nodes.
 * @param {Object[]} [data.extra_parents] - The extra parent nodes.
 *
 * @example
 * <GraphVisualisation :data="data" />
 */
export default {
  name: 'GraphVisualisation'
}
</script>

<template>
  <div id="tree-container">
    <svg ref="svgRef"></svg>
  </div>
</template>

<style scoped>
.node circle {
  fill: #999;
}

.node text {
  font-size: 12px;
  color: #555;
}

.link {
  fill: none;
  stroke: #555;
  stroke-width: 1.5px;
  stroke-opacity: 0.4;
}
</style>
