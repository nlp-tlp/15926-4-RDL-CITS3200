<template>
  <div id="app">
    <!-- Button to capture screen -->
    <button @click="captureScreen">Capture Screen</button>

    <!-- Modal for preview -->
    <div v-if="isPreviewVisible" class="modal">
      <div class="modal-content">
        <span class="close" @click="closePreview">&times;</span>
        <h3>Screenshot Preview</h3>
        <img :src="screenshotDataUrl" alt="Screenshot Preview" class="screenshot-preview" />

        <!-- Dropdown for file type selection -->
        <select v-model="selectedFileType">
          <option value="png">PNG</option>
          <option value="jpeg">JPEG</option>
          <option value="svg">SVG</option>
        </select>

        <!-- Save button -->
        <button @click="saveScreenshot">Save</button>
      </div>
    </div>
    <div id="captureArea">
      <svg ref="svgRef"></svg>
    </div>
  </div>
</template>

<script setup lang="ts">
import * as d3 from 'd3'
import { saveAs } from 'file-saver'
import html2canvas from 'html2canvas'
import { onMounted, ref } from 'vue'

const props = defineProps({
  data: {
    type: Object,
    required: true
  }
})

const selectedFileType = ref('png') // Selected file type for export
const isPreviewVisible = ref(false) // Toggle to show/hide the preview modal
const screenshotDataUrl = ref('') // Store the data URL of the screenshot

// Function to capture the screen and show the preview modal
const captureScreen = () => {
  const captureArea = document.getElementById('captureArea')

  if (captureArea) {
    html2canvas(captureArea, {
      scale: 2 // Increase scale for better quality
    }).then((canvas) => {
      screenshotDataUrl.value = canvas.toDataURL(`image/${selectedFileType.value}`)
      isPreviewVisible.value = true // Show the preview modal
    })
  }
}

// Function to save the screenshot based on the selected file type
const saveScreenshot = () => {
  const canvas = document.createElement('canvas')
  const img = new Image()
  img.src = screenshotDataUrl.value

  img.onload = () => {
    canvas.width = img.width
    canvas.height = img.height
    const ctx = canvas.getContext('2d')
    ctx?.drawImage(img, 0, 0)

    canvas.toBlob((blob) => {
      if (blob) {
        const fileName = `screenshot.${selectedFileType.value}`
        saveAs(blob, fileName) // Save the image
      }
    }, `image/${selectedFileType.value}`)
  }
}

// Function to close the preview modal
const closePreview = () => {
  isPreviewVisible.value = false
}

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

  // Add arrowhead marker
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

  function zoomed(event: any) {
    svg.attr('transform', event.transform)
  }

  const root = d3.hierarchy(data)

  function update(source: any) {
    // Assigns the x and y position for the nodes
    const treeLayout = d3.tree().nodeSize([nodeDistance, 300])
    const treeData = treeLayout(root as unknown as d3.HierarchyNode<unknown>)

    // Compute the new tree layout.
    const nodes = treeData.descendants()
    const links = treeData.links()

    // Normalize for fixed-depth.
    nodes.forEach((d) => (d.y = d.depth * 180))

    // ********** Nodes section **********

    const node = svg.selectAll('g.node').data(nodes, (d: any) => d.id || (d.id = d.data.name))

    // Enter any new nodes at the parent's previous position.
    const nodeEnter: any = node
      .enter()
      .append('g')
      .attr('class', 'node')
      .on('click', (event, d) => toggleCollapse(d))
      .style('cursor', (d: any) => (d.children || d._children ? 'pointer' : 'default'))

    // Add Circle for the nodes
    nodeEnter
      .append('circle')
      .attr('r', 5)
      .style('fill', (d: any) => (d._children ? 'lightsteelblue' : '#999'))

    // Add labels for the nodes
    nodeEnter
      .append('text')
      .attr('dy', '.35em')
      .attr('x', (d: any) => (d.children || d._children ? -10 : 10))
      .style('text-anchor', (d: any) => (d.children || d._children ? 'end' : 'start'))
      .text((d: any) => d.data.name)

    // Update the node positions
    const nodeUpdate = nodeEnter.merge(node)

    nodeUpdate.attr('transform', (d: any) => `translate(${d.y},${d.x})`)

    // Update the node attributes and style
    nodeUpdate
      .select('circle')
      .attr('r', 5)
      .style('fill', (d: any) => (d._children ? 'lightsteelblue' : '#999'))

    // Remove any exiting nodes
    const nodeExit = node.exit().remove()

    nodeExit.select('circle').attr('r', 0)

    nodeExit.select('text').style('fill-opacity', 0)

    // ********** Links section **********

    const link: any = svg.selectAll('path.link').data(links, (d: any) => d.target.id)

    // Enter new links at the parent's previous position.
    const linkEnter = link
      .enter()
      .insert('path', 'g')
      .attr('class', 'link')
      .attr('stroke', 'black')
      .attr('fill', 'none')
      .attr('marker-end', 'url(#arrow)') // Added attribute for arrow head

    // Update links
    const linkUpdate = linkEnter.merge(link)

    linkUpdate.attr('d', diagonal)

    // Remove exiting links
    link
      .exit()
      .attr('d', () => {
        const o = { x: source.x, y: source.y }
        return diagonal({ source: o, target: o })
      })
      .remove()

    const extraLinks: any = []
    nodes.forEach((d: any) => {
      if (d.data.extra_parents) {
        d.data.extra_parents.forEach((parent: any) => {
          const parentNode = nodes.find((node: any) => node.data.name === parent.name)
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
      .attr('marker-end', 'url(#arrow)') // Added attribute for arrow head
      .attr('d', (d: any) => diagonal({ source: d.source, target: d.target }))

    extraLink
      .merge(extraLink)
      .attr('d', (d: any) => diagonal({ source: d.source, target: d.target }))

    //Remove any exiting extra links
    extraLink.exit().remove()
  }

  // Toggle children on click.
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

  // Start the rendering
  update(root)

  const endTime = performance.now()
  console.log(`Rendering took ${endTime - startTime} ms`)
})
</script>

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

/* Modal Styles */
.modal {
  position: fixed;
  z-index: 1000;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
  width: 1000px;
  background-color: white;
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  padding: 1rem;
}

.modal-content {
  text-align: center;
}

.close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  cursor: pointer;
  font-size: 1.5rem;
}

.screenshot-preview {
  width: 100%;
  margin-bottom: 1rem;
}

/* Button Styles */
button {
  width: 100px;
  padding: 0.5rem 1rem;
  background-color: var(--color-nav-background);
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  color: var(--color-nav-text-active);
}

select {
  margin-bottom: 1rem;
  padding: 0.3rem;
  width: 100%;
  border-radius: 5px;
}
</style>
