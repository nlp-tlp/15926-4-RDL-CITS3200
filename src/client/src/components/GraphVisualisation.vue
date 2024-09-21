<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  fetchChildren: {
    type: Function,
    required: true
  }
})

const svgRef = ref<Element>()

const width = window.innerWidth
const height = window.innerHeight
const nodeDistance = 20
const initialGraphX = (width / 7) * 1
const initialGraphY = (height / 7) * 3

let svg: any
let root: any

onMounted(() => {
  initialiseGraph()
  initialGraphRender()
})

watch(
  () => props.data,
  (newData) => {
    if (newData) {
      updateGraph()
    }
  }
)

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
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'black')

  d3.select(svgRef.value as Element).call(d3.zoom().transform as any, initialTransform)
}

function zoomed(event: any) {
  svg.attr('transform', event.transform)
}

function initialGraphRender() {
  if (!props.data) {
    return
  }
  root = d3.hierarchy(props.data)
  update(root)
}

function updateGraph() {
  if (!props.data) {
    return
  }
  root = d3.hierarchy(props.data)
  update(root)
}

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

async function toggleCollapse(d: any) {
  if (d.children) {
    // Collapse the node
    d._children = d.children
    d.children = null
  } else {
    // if node has children
    if (d.data.has_children) {
      // if children are not loaded yet
      if (!d.children) {
        await props.fetchChildren(d.data)
      }
      // Expand the node
      d.children = d._children
      d._children = null
    } else {
      // if node has no children
      console.log('Node has no children:', d.data)
      return
    }
  }

  // Trigger the update to re-render the graph with the updated node
  update(d)
  console.log('Toggled node:', d.data)
}

function renderNodes(nodes: any) {
  const node = svg.selectAll('g.node').data(nodes, (d: any) => d.id || (d.id = d.data.id))

  const nodeEnter: any = node
    .enter()
    .append('g')
    .attr('class', 'node')
    .on('click', (event: Event, d: any) => toggleCollapse(d))

  nodeEnter
    .append('circle')
    .attr('r', 5)
    .style('fill', (d: any) => (d.data.has_children ? 'lightsteelblue' : '#999'))
    .style('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))

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
    .style('fill', (d: any) => (d.data.has_children ? 'lightsteelblue' : '#999'))

  nodeUpdate
    .select('text')
    .attr('x', (d: any) => (d.children || d._children ? -10 : 10))
    .style('text-anchor', (d: any) => (d.children || d._children ? 'end' : 'start'))

  node.exit().remove()
}

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

const diagonal: any = d3
  .linkHorizontal()
  .x((d: any) => d.y)
  .y((d: any) => d.x)
</script>

<script lang="ts">
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
