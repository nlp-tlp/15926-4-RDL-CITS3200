<template>
  <div>
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
  </div>
</template>

<script setup lang="ts">
import { saveAs } from 'file-saver'
import { ref } from 'vue'

// **Props**
const props = defineProps({
  /**
   * Reference to the SVG element to be exported.
   */
  svgRef: {
    type: SVGSVGElement,
    required: true
  }
})

const selectedFileType = ref('png') // Selected file type for export
const isPreviewVisible = ref(false) // Toggle to show/hide the preview modal
const screenshotDataUrl = ref('') // Store the data URL of the screenshot
const isLoading = ref(false)
const isScaled = ref(false)

// Function to inline all styles into the SVG
const inlineStyles = (element: SVGElement) => {
  const cssStyleSheets = Array.from(document.styleSheets).filter(
    (styleSheet) => !styleSheet.href || styleSheet.href.startsWith(window.location.origin)
  )

  const cssRules: CSSRule[] = []

  cssStyleSheets.forEach((styleSheet) => {
    try {
      const sheetRules = styleSheet.cssRules
      if (sheetRules) {
        cssRules.push(...Array.from(sheetRules))
      }
    } catch (e) {
      console.warn('Could not access CSS rules from stylesheet:', styleSheet.href)
    }
  })

  cssRules.forEach((rule) => {
    if (rule instanceof CSSStyleRule) {
      const elements = element.querySelectorAll(rule.selectorText)
      elements.forEach((el: any) => {
        rule.style.cssText.split(';').forEach((style) => {
          const [property, value] = style.split(':')
          if (property && value) {
            el.style.setProperty(property.trim(), value.trim())
          }
        })
      })
    }
  })
}

const captureScreen = () => {
  const svgElement = props.svgRef
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
  const svgElement = props.svgRef
  if (!svgElement) return

  if (selectedFileType.value === 'svg') {
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

    // Inline all styles into the cloned SVG
    inlineStyles(clonedSvgElement)

    // Serialize the cloned SVG into a string
    const serializer = new XMLSerializer()
    const svgString = serializer.serializeToString(clonedSvgElement)

    // Create a Blob and save the SVG
    const blob = new Blob([svgString], { type: 'image/svg+xml;charset=utf-8' })
    saveAs(blob, 'graph.svg')
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
</script>

<style scoped>
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
