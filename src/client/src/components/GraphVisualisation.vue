<template>
  <div id="app">
    <!-- Capture Screen Button -->
    <button class="capture-button" @click="captureScreen">Capture Screen</button>

    <div v-if="isLoading" class="spinner"></div>

    <!-- Preview Modal -->
    <div v-if="isPreviewVisible" class="modal-overlay" @click.self="closePreview">
      <div class="modal-content">
        <span class="close" @click="closePreview">&times;</span>
        <h3>Screenshot Preview</h3>
        <img :src="screenshotDataUrl" alt="Screenshot Preview" class="screenshot-preview" />

        <!-- Warning Message -->
        <div v-if="isScaled" class="warning">
          <p>
            <strong>Warning:</strong> The image has been scaled down due to size limitations. The
            exported image may be lower resolution for PNG/JPEG. Please export as SVG.
          </p>
        </div>

        <!-- Dropdown for file type -->
        <select v-model="selectedFileType">
          <option value="png">PNG</option>
          <option value="jpeg">JPEG</option>
          <option value="svg">SVG</option>
        </select>

        <!-- Save button on Modal -->
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
// import html2canvas from 'html2canvas'
import { onMounted, ref, watch } from 'vue'

const props = defineProps({
  /**
   * The reactive data object to be visualised; with some initial data.
   */
  data: {
    type: Object,
    required: true
  },
  /**
   * Function to fetch the children of a node from the server.
   */
  fetchChildren: {
    type: Function,
    required: true
  },
  /**
   * Indicates whether to show labels in the graph.
   */
  showLabels: {
    type: Boolean,
    default: true
  }
})

const selectedFileType = ref('png') // Selected file type for export
const isPreviewVisible = ref(false) // Toggle to show/hide the preview modal
const screenshotDataUrl = ref('') // Store the data URL of the screenshot
const isLoading = ref(false)
const isScaled = ref(false)

// Function to inline all styles into the SVG
//(Styles from our d3 graph have to be put inline to export as a SVG)
const inlineStyles = (element: SVGElement) => {
  const cssStyleSheets = Array.from(document.styleSheets).filter(
    (styleSheet) => !styleSheet.href || styleSheet.href.startsWith(window.location.origin)
  );

  const cssRules: CSSRule[] = [];

  cssStyleSheets.forEach((styleSheet) => {
    try {
      const sheetRules = styleSheet.cssRules;
      if (sheetRules) {
        cssRules.push(...Array.from(sheetRules));
      }
    } catch (e) {
      console.warn('Could not access CSS rules from stylesheet:', styleSheet.href);
    }
  });

  cssRules.forEach((rule) => {
    if (rule instanceof CSSStyleRule) {
      const elements = element.querySelectorAll(rule.selectorText);
      elements.forEach((el: any) => {
        rule.style.cssText.split(';').forEach((style) => {
          const [property, value] = style.split(':');
          if (property && value) {
            el.style.setProperty(property.trim(), value.trim());
          }
        });
      });
    }
  });
};


const captureScreen = () => {
  const svgElement = svgRef.value
  if (svgElement) {
    // Inline all styles into the SVG element
    inlineStyles(svgElement)

    // Get the bounding box of the <g> element
    const gElement = svgElement.querySelector('g')
    if (!gElement) {
      console.error('No <g> element found in the SVG.')
      return
    }
    const bbox = gElement.getBBox()

    // Clone the SVG element
    const clonedSvgElement = svgElement.cloneNode(true) as SVGSVGElement
    const clonedGElement = clonedSvgElement.querySelector('g')
    if (!clonedGElement) {
      console.error('No <g> element found in the cloned SVG.')
      return
    }

    // Apply padding
    const padding = 20
    const minX = bbox.x - padding
    const minY = bbox.y - padding
    const width = bbox.width + 5 * padding
    const height = bbox.height + 2 * padding

    // Adjust the 'transform' to shift the graph into the view
    clonedGElement.setAttribute('transform', `translate(${-minX},${-minY})`)

    // Adjust the cloned SVG's width, height, and viewBox
    clonedSvgElement.setAttribute('width', width.toString())
    clonedSvgElement.setAttribute('height', height.toString())
    clonedSvgElement.setAttribute('viewBox', `0 0 ${width} ${height}`)

    // Serialize the cloned SVG into a string
    const svgData = new XMLSerializer().serializeToString(clonedSvgElement)

    // Create a new canvas element
    const canvas = document.createElement('canvas')
    canvas.width = width
    canvas.height = height
    const ctx = canvas.getContext('2d')
    if (!ctx) {
      console.error('Failed to get 2D context')
      return
    }

    // Handle canvas size limitations
    const MAX_CANVAS_SIZE = 8192 // Or the maximum size supported by the browser
    let scaleFactor = 1
    if (width > MAX_CANVAS_SIZE || height > MAX_CANVAS_SIZE) {
      scaleFactor = Math.min(MAX_CANVAS_SIZE / width, MAX_CANVAS_SIZE / height)
      canvas.width = width * scaleFactor
      canvas.height = height * scaleFactor
      ctx.scale(scaleFactor, scaleFactor)
      isScaled.value = true // Image was scaled
    } else {
      canvas.width = width
      canvas.height = height
      isScaled.value = false // Image was not scaled
    }

    // Create an Image object from the serialized SVG
    const img = new Image()
    img.src = 'data:image/svg+xml;base64,' + btoa(unescape(encodeURIComponent(svgData)))

    img.onload = () => {
      // Draw the SVG image onto the canvas
      ctx.drawImage(img, 0, 0)

      // Convert the canvas to a data URL for the screenshot preview
      screenshotDataUrl.value = canvas.toDataURL(`image/${selectedFileType.value}`)
      isPreviewVisible.value = true
      isLoading.value = false
    }

    img.onerror = () => {
      console.error('Image failed to load.')
      isLoading.value = false
    }
  }
}

const saveScreenshot = () => {
  if (selectedFileType.value === 'svg') {
    const svgElement = svgRef.value;
    if (!svgElement) return;

    // Inline all styles into the SVG element
    inlineStyles(svgElement);

    // Get the bounding box of the <g> element
    const gElement = svgElement.querySelector('g');
    if (!gElement) {
      console.error('No <g> element found in the SVG.');
      return;
    }
    const bbox = gElement.getBBox();

    // Clone the SVG element
    const clonedSvgElement = svgElement.cloneNode(true) as SVGSVGElement;
    const clonedGElement = clonedSvgElement.querySelector('g');
    if (!clonedGElement) {
      console.error('No <g> element found in the cloned SVG.');
      return;
    }

    // Apply padding
    const padding = 20;
    const minX = bbox.x - padding;
    const minY = bbox.y - padding;
    const width = bbox.width + 5 * padding;
    const height = bbox.height + 2 * padding;

    // Adjust the 'transform' to shift the graph into the view
    clonedGElement.setAttribute('transform', `translate(${-minX},${-minY})`);

    // Adjust the cloned SVG's width, height, and viewBox
    clonedSvgElement.setAttribute('width', width.toString());
    clonedSvgElement.setAttribute('height', height.toString());
    clonedSvgElement.setAttribute('viewBox', `0 0 ${width} ${height}`);

    // Inline all styles into the cloned SVG
    inlineStyles(clonedSvgElement);

    // Serialize the cloned SVG into a string
    const serializer = new XMLSerializer();
    const svgString = serializer.serializeToString(clonedSvgElement);

    // Create a Blob and save the SVG
    const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' });
    saveAs(blob, 'graph.svg');
  } else {
    // Save PNG/JPEG from canvas data
    const canvas = document.createElement('canvas')
    const img = new Image()
    img.src = screenshotDataUrl.value

    img.onload = () => {
      canvas.width = img.width
      canvas.height = img.height
      const ctx = canvas.getContext('2d')
      if (!ctx) {
        console.error('Failed to get 2D context')
        return
      }

      // Fill the canvas with white background
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

      // Draw the image onto the canvas
      ctx.drawImage(img, 0, 0)

      canvas.toBlob(
        (blob) => {
          if (blob) {
            const fileName = `screenshot.${selectedFileType.value}`
            saveAs(blob, fileName)
          }
        },
        `image/${selectedFileType.value}`,
        1 // Quality parameter for JPEG (0 to 1), optional for PNG
      )
    }

    img.onerror = () => {
      console.error('Image failed to load.')
    }
  }
}

// Function to close the preview modal
const closePreview = () => {
  isPreviewVisible.value = false
}

// Reference to the SVG elemen
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
  renderGraph()
})

// Watch for changes in the data object and re-render the graph
watch(
  () => props.data,
  (newData) => {
    if (newData) {
      renderGraph()
    }
  }
)

/**
 * Initialise the graph with the SVG element and reposition it to the center vertically.
 */
function initialiseGraph() {
  svg = d3
    .select(svgRef.value as SVGSVGElement)
    .attr('width', width)
    .attr('height', height)
    .call(d3.zoom().scaleExtent(zoomScale).on('zoom', zoomed) as any)
    .append('g')
    .attr('transform', d3.zoomIdentity.translate(initialGraphX, initialGraphY).toString())

  // Add the arrow marker for the links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 19.5)
    .attr('refY', 0)
    .attr('markerWidth', 6)
    .attr('markerHeight', 6)
    .attr('orient', 'auto')
    .attr('markerUnits', 'strokeWidth')
    .append('path')
    .attr('d', 'M0,-5L10,0L0,5')
    .attr('fill', 'black')

  // add arrow marker for extra links
  svg
    .append('defs')
    .append('marker')
    .attr('id', 'arrow-extra')
    .attr('viewBox', '0 -5 10 10')
    .attr('refX', 19.5)
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
 * Zoom the graph.
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

/**
 * Render the graph with the data object from the props.
 */
function renderGraph() {
  // Check if the data object is available
  if (!props.data) {
    return
  }

  // Create a hierarchy from the data object
  root = d3.hierarchy(props.data)
  // update the graph based on the new data in the props
  update(root)
}

/**
 * Update the graph with the new data.
 * @param source The source node.
 */
function update(source: any) {
  // Create a tree layout with the node distance
  const treeLayout = d3.tree().nodeSize([nodeDistanceX, nodeDistanceY])
  const treeData = treeLayout(root as unknown as d3.HierarchyNode<unknown>)

  // Get the nodes and links
  const nodes = treeData.descendants()
  const links = treeData.links()

  // Render the nodes, links, and extra links
  renderNodes(nodes)
  renderLinks(links)
  renderExtraLinks(nodes)

  // re collapse the nodes that were previously collapsed for consistency
  hidePreviousCollapsedNodes(nodes)
}

/**
 * Hide the nodes that were previously collapsed.
 * @param nodes The nodes to be checked.
 */
function hidePreviousCollapsedNodes(nodes: any) {
  nodes.forEach((d: any) => {
    // Check if the node was previously collapsed but the children are currently visible
    if (d.data.expanded === false && d.children) {
      d._children = d.children
      d.children = null
    }
  })
}

/**
 * Toggle the collapse of a node.
 * @param node The node to be toggled.
 */
async function toggleCollapse(node: any) {
  // Check if the node has children
  if (node.data.has_children) {
    // Check if the children have not been fetched
    if (!node.children && !node._children) {
      // Fetch the children of the node
      await props.fetchChildren(node.data)

      // Expand the node
      node.children = node._children
      node._children = null
      node.data.expanded = true
      console.log('Expanded node:', node.data.label)
    } else {
      // if the children are hidden
      if (node._children) {
        // Expand the node
        node.children = node._children
        node._children = null
        node.data.expanded = true
        console.log('Expanded node:', node.data.label)
      }
      // if the children are visible
      else if (node.children) {
        // Collapse the node
        node._children = node.children
        node.children = null
        node.data.expanded = false
        console.log('Collapsed node:', node.data.label)
      }
    }
  } else {
    // if the node has no children
    console.log('Node has no children:', node.data.label)
    return
  }
  // Trigger the update to re-render the graph with the changes
  update(node)
}

/**
 * Render the nodes of the graph.
 * @param nodes The nodes to be rendered.
 */
function renderNodes(nodes: any) {
  // Select all nodes and bind the data
  const node = svg.selectAll('g.node').data(nodes, (d: any) => d.id)

  // on enter, append the node group and add the circle and text elements
  const nodeEnter: any = node
    .enter()
    .append('g')
    .attr('class', 'node')
    // on click, toggle the collapse of the node
    .on('click', (event: Event, d: any) => toggleCollapse(d))

  nodeEnter
    .append('circle')
    .attr('r', nodeRadius)
    // set the fill color based on the presence of children
    .style('fill', (d: any) => (d.data.has_children ? 'lightsteelblue' : '#999'))
    // set the cursor style based on the presence of children
    .style('cursor', (d: any) => (d.data.has_children ? 'pointer' : 'default'))
    .on('mouseover', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement).style('fill', 'lightblue')
    })
    .on('mouseout', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement).style('fill', (d: any) =>
        d.data.has_children ? 'lightsteelblue' : '#999'
      )
    })
    .on('click', (event: any, d: any) => {
      event.stopPropagation() // Prevents bubbling
      toggleCollapse(d)
    })

  nodeEnter
    .append('text')
    .attr('dy', '.35em')
    // set the text position based on the expanded state - left if expanded, right if collapsed
    .attr('x', (d: any) => (d.data.expanded ? -10 : 10))
    .style('text-anchor', (d: any) => (d.data.expanded ? 'end' : 'start'))
    .style('cursor', () => 'pointer')
    .text((d: any) => d.data.label)
    .on('mouseover', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement)
        .style('fill', 'lightblue')
        .style('font-weight', 'bold')
    })
    .on('mouseout', (event: MouseEvent) => {
      d3.select(event.currentTarget as SVGTextElement)
        .style('fill', '')
        .style('font-weight', 'normal')
    })
    .on('click', (event: any, d: any) => {
      event.stopPropagation()
      handleLabelClick(d)
    })

  // merge the enter and update selections
  const nodeUpdate = nodeEnter.merge(node)

  // update the node positions
  nodeUpdate.attr('transform', (d: any) => `translate(${d.y},${d.x})`)

  // update visibility of labels based on showLabels prop
  nodeUpdate.select('text').style('display', props.showLabels ? 'block' : 'none')

  // remove the nodes that are no longer needed
  node.exit().remove()
}

const emit = defineEmits(['label-clicked'])

function handleLabelClick(node: any) {
  emit('label-clicked', node.data.id)
}

/**
 * Render the links of the graph.
 * @param links The links to be rendered.
 */
function renderLinks(links: any, colour: string = '#999') {
  // Select all links and bind the data
  const link: any = svg.selectAll('path.link').data(links, (d: any) => d.target.id)

  // on enter, insert the path element and set the attributes
  const linkEnter = link
    .enter()
    .insert('path', 'g')
    .attr('class', 'link')
    .attr('stroke', colour)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow)')

  // merge the enter and update selections
  const linkUpdate = linkEnter.merge(link)

  linkUpdate.attr('d', diagonal)

  link.exit().remove()
}

/**
 * Render the extra links of the graph.
 * @param nodes The nodes to be used for the extra links.
 */
function renderExtraLinks(nodes: any, colour: string = 'red') {
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
    .attr('stroke', colour)
    .attr('fill', 'none')
    .attr('marker-end', 'url(#arrow-extra)')
    .attr('stroke-dasharray', '5,5')

  // merge the enter and update selections
  const extraLinkUpdate = extraLinkEnter.merge(extraLink)

  // update the extra link positions to use the diagonal function
  extraLinkUpdate.attr('d', diagonal)

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

<style>
.link {
  fill: none;
  stroke: #555;
  stroke-width: 1.5px;
  stroke-opacity: 0.4;
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent background */
  display: flex;
  align-items: center;
  justify-content: center;
}
/* Modal Content Styles */
.modal-content {
  background-color: white;
  width: 60%;
  max-width: 90vw;
  max-height: 90vh;
  overflow: auto;
  padding: 1rem;
  position: relative; /* For the close button positioning */
  border: 1px solid #ccc;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  text-align: center;
}

/* Close Button Styles */
.close {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
  cursor: pointer;
  font-size: 1.5rem;
}

/* Screenshot Preview Styles */
.screenshot-preview {
  width: 100%;
  margin-bottom: 1rem;
}

/* Warning Message Styles */
.warning {
  background-color: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
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

.capture-button {
  position: fixed;
  right: 20px;
  bottom: 20px;
}

button:hover {
  color: var(--color-nav-text-active);
}

/* Select Styles */
select {
  margin-bottom: 1rem;
  padding: 0.3rem;
  width: 100%;
  border-radius: 5px;
  border: 1px solid black;
}

/* Spinner Styles */
.spinner {
  border: 4px solid rgba(0, 0, 0, 0.1);
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}

@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
