<template>
  <div>
    <!-- Capture Screen Button -->
    <button
      class="w-3 p-2 bg-none text-w border-none rounded-md cursor-pointer hover:color-nav-text-active fixed right-6 bottom-6"
      @click="captureScreen"
    >
      <svg
        class="svg-icon"
        style="
          width: 1.5em;
          height: 1.5em;
          vertical-align: middle;
          fill: var(--color-nav-background);
          overflow: hidden;
        "
        viewBox="0 0 1024 1024"
        version="1.1"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M471 250.4c0-22.1 17.9-40.1 40.1-40.1 22.1 0 40.1 17.9 40.1 40.1V680c0 22.1-17.9 40.1-40.1 40.1-22.1 0-40.1-17.9-40.1-40.1V250.4z m0 429.5"
        />
        <path
          d="M852.5 834V645.4c0-20.8 16.9-37.7 37.7-37.7 20.8 0 37.7 16.9 37.7 37.7v226.2c0 20.8-16.9 37.7-37.7 37.7H136.1c-20.8 0-37.7-16.9-37.7-37.7V645.4c0-20.8 16.9-37.7 37.7-37.7 20.8 0 37.7 16.9 37.7 37.7V834h678.7z m0 0M511.1 229.5L320.3 437.9c-15.1 16.4-40.5 17.4-56.9 2.4-16.4-15-17.5-40.5-2.4-56.9L481.4 143c7.6-8.4 18.4-13.1 29.7-13.1s22.1 4.8 29.6 13.1l220.4 240.4c15 16.4 14 41.9-2.4 56.9s-41.9 14-56.9-2.4L511.1 229.5z m190.7 208.4"
        />
      </svg>
    </button>

    <!-- Preview Modal -->
    <div
      v-if="isPreviewVisible"
      class="fixed z-50 inset-0 w-full h-full bg-black bg-opacity-50 flex items-center justify-center"
      @click.self="closePreview"
    >
      <div
        class="bg-white w-3/5 max-w-[90vw] max-h-[90vh] flex flex-col relative border-none shadow-md text-center rounded-lg"
      >
        <!-- Modal header -->
        <div class="absolute top-0 left-0 w-full bg-nav-background text-white p-3 rounded-t-lg">
          <span class="absolute top-3 right-3 cursor-pointer" @click="closePreview">&times;</span>
          <h3>Export Preview</h3>
        </div>

        <!-- Modal content -->
        <div class="flex-1 overflow-auto mt-12 p-4">
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
        </div>

        <!-- Modal footer -->
        <div class="p-2 bg-nav-background rounded-b-lg">
          <!-- Dropdown for file type -->
          <select
            v-model="selectedFileType"
            class="p-1.5 w-24 mx-2 rounded-md border border-gray-200 bg-cyan-950 text-gray-200"
          >
            <option value="png">PNG</option>
            <option value="jpeg">JPEG</option>
            <option value="svg">SVG</option>
          </select>

          <!-- Save button on Modal -->
          <button
            class="w-24 p-1.5 bg-cyan-950 text-gray-200 border border-gray-200 rounded-md cursor-pointer hover:color-nav-text-active"
            @click="saveScreenshot"
          >
            Export
          </button>
        </div>
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
