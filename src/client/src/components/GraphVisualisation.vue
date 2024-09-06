<template>
  <div id="tree-container">
    <svg ref="svgRef"></svg>
  </div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { onMounted, ref } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const svgRef = ref(null)

// width and height to fit the whole parent container
const width = window.innerWidth
const height = window.innerHeight
const nodeDistance = 10

const data = props.data

onMounted(() => {
  const startTime = performance.now()
  const svg = d3
    .select(svgRef.value)
    .attr('width', width)
    .attr('height', height)
    .call(d3.zoom().scaleExtent([0.5, 5]).on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', 'translate(40,0)')

  function zoomed(event: any) {
    svg.attr('transform', event.transform)
  }

  const root = d3.hierarchy(data)

  const treeLayout = d3.tree().nodeSize([nodeDistance, 300])
  treeLayout(root as unknown as d3.HierarchyNode<unknown>)

  const nodeById: { [key: string]: any } = {}
  root.each((d) => {
    nodeById[d.data.name] = d
  })

  const linkPathGenerator: any = d3
    .linkHorizontal()
    .x((d: any) => d.y)
    .y((d: any) => d.x)

  svg
    .selectAll('path.link')
    .data(root.links())
    .enter()
    .append('path')
    .attr('class', 'link')
    .attr('d', linkPathGenerator)
    .attr('stroke', 'black')
    .attr('fill', 'none')

  svg
    .selectAll('g.node')
    .data(root.descendants())
    .enter()
    .append('g')
    .attr('class', 'node')
    .attr('transform', (d) => `translate(${d.y},${d.x})`)
    .append('circle')
    .attr('r', 5)

  svg
    .selectAll('g.node')
    .append('text')
    .attr('dy', '.35em')
    .attr('x', (d: any) => (d.children ? -10 : 10))
    .style('text-anchor', (d: any) => (d.children ? 'end' : 'start'))
    .text((d: any) => d.data.name)
    .attr('stroke', 'white')
    .attr('paint-order', 'stroke')

  const extraLinks: Array<any> = []

  root.descendants().forEach((d) => {
    if (d.data.extra_parents) {
      d.data.extra_parents.forEach((parent: { name: string | number }) => {
        const parentNode = nodeById[parent.name]
        if (parentNode) {
          extraLinks.push({ source: parentNode, target: d })
        }
      })
    }
  })

  svg
    .selectAll('path.extra-link')
    .data(extraLinks)
    .enter()
    .append('path')
    .attr('class', 'link') // Same style as the normal links
    .attr('d', (d) => linkPathGenerator({ source: d.source, target: d.target }))
    .attr('stroke', 'black')
    .attr('fill', 'none')

  const endTime = performance.now()
  console.log(`Rendering took ${endTime - startTime} ms`)
})
</script>

<style scoped>
body {
  font-family: Arial, sans-serif;
}

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
