<template>
  <div>
    <!-- Capture Screen Button -->
    <button
      class="w-24 px-4 py-2 bg-nav-background text-white border-none rounded-md cursor-pointer hover:color-nav-text-active fixed right-5 bottom-5"
      @click="captureScreen"
    >
      Capture Screen
    </button>

    <!-- <div v-if="isLoading" class="spinner"></div> -->
    <div v-if="isLoading" class="fixed inset-0 flex items-center justify-center">
      <div
        class="w-10 h-10 border-4 border-gray-200 border-t-blue-500 rounded-full animate-spin"
      ></div>
    </div>

    <!-- Preview Modal -->
    <div
      v-if="isPreviewVisible"
      class="fixed z-50 inset-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
      @click.self="closePreview"
    >
      <div
        class="bg-white w-3/5 max-w-[90vw] max-h-[90vh] overflow-auto p-4 relative border border-black shadow-md text-center rounded-lg"
      >
        <span class="absolute top-2 right-2 cursor-pointer" @click="closePreview">&times;</span>
        <h3>Screenshot Preview</h3>

        <!-- Warning Message -->
        <div
          v-if="isScaled"
          class="bg-amber-200 text-yellow-800 border-yellow-200 p-2.5 mb-3.5 rounded-md"
        >
          <p>
            <strong>Warning:</strong> The image has been scaled down due to size limitations. The
            exported image may be lower resolution for PNG/JPEG. Please export as SVG to preserve
            resolution.
          </p>
        </div>

        <img :src="screenshotDataUrl" alt="Screenshot Preview" class="w-full mb-4" />

        <!-- Dropdown for file type -->
        <select
          v-model="selectedFileType"
          class="mb-4 p-1.5 w-full rounded-md border border-gray-200"
        >
          <option value="png">PNG</option>
          <option value="jpeg">JPEG</option>
          <option value="svg">SVG</option>
        </select>

        <!-- Save button on Modal -->
        <button
          class="w-24 px-4 py-2 bg-nav-background text-white border-none rounded-md cursor-pointer hover:color-nav-text-active"
          @click="saveScreenshot"
        >
          Save
        </button>
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
  // Start the spinner
  isLoading.value = true

  const svgElement = props.svgRef
  if (svgElement) {
    // Inline all styles into the SVG element
    inlineStyles(svgElement)

    // Get the bounding box of the <g> element
    const gElement = svgElement.querySelector('g')
    if (!gElement) {
      console.error('No <g> element found in the SVG.')
      isLoading.value = false // Stop the spinner
      return
    }
    const bbox = gElement.getBBox()

    // Clone the SVG element
    const clonedSvgElement = svgElement.cloneNode(true) as SVGSVGElement
    const clonedGElement = clonedSvgElement.querySelector('g')
    if (!clonedGElement) {
      console.error('No <g> element found in the cloned SVG.')
      isLoading.value = false // Stop the spinner
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
      isLoading.value = false // Stop the spinner
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
      // Fill the canvas with white background (fixes bug)
      ctx.fillStyle = 'white'
      ctx.fillRect(0, 0, canvas.width, canvas.height)

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
@keyframes spin {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>
